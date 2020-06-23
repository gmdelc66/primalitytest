/*
This file is part of Alpertron Calculators.

Copyright 2018 Dario Alejandro Alpern

Alpertron Calculators is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Alpertron Calculators is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Alpertron Calculators.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "bignbr.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define FFT_LIMB_SIZE   19
#define FFT_LIMB_RANGE  (1 << FFT_LIMB_SIZE)
#define MAX_VALUE_FFT_LIMB (FFT_LIMB_RANGE - 1)
#define MAX_FFT_LEN        (MAX_LEN * BITS_PER_GROUP / FFT_LIMB_SIZE + 10)
typedef struct sComplex
{
  double real;
  double imaginary;
} complex;

struct sCosSin
{
  int Cos[2];
  int Sin[2];
};

#define POWERS_2       17
#define QUARTER_CIRCLE (1 << (POWERS_2 - 2))
#define HALF_CIRCLE    (1 << (POWERS_2 - 1))
#define CIRCLE_MASK    ((1 << POWERS_2) - 1)
// In the next array, all numbers are represented by two elements,
// first the least significant limb, then the most significant limb.
struct sCosSin cossinPowerOneHalf[] =
{
  {{2121767201, 1518500249}, {2121767201, 1518500249}},  // cos(pi/2^2), then sin(pi/2^2)
  {{1696238673, 1984016188}, {782852817, 821806413}},    // cos(pi/2^3), then sin(pi/2^3)
  {{1857642581, 2106220351}, {886244699, 418953276}},    // cos(pi/2^4), then sin(pi/2^4)
  {{575294268, 2137142927}, {174918392, 210490206}},     // cos(pi/2^5), then sin(pi/2^5)
  {{1926953927, 2144896909}, {565903996, 105372028}},    // cos(pi/2^6), then sin(pi/2^6)
  {{161094006, 2146836866}, {2050385887, 52701886}},     // cos(pi/2^7), then sin(pi/2^7)
  {{925218478, 2147321946}, {1727413283, 26352927}},     // cos(pi/2^8), then sin(pi/2^8)
  {{487924890, 2147443222}, {2040267204, 13176711}},     // cos(pi/2^9), then sin(pi/2^9)
  {{1144652709, 2147473541}, {2107197812, 6588386}},     // cos(pi/2^10), then sin(pi/2^10)
  {{819842189, 2147481121}, {786843437, 3294197}},       // cos(pi/2^11), then sin(pi/2^11)
  {{741631965, 2147483016}, {360077744, 1647099}},       // cos(pi/2^12), then sin(pi/2^12)
  {{185395523, 2147483490}, {1383830441, 823549}},       // cos(pi/2^13), then sin(pi/2^13)
  {{1120089925, 2147483608}, {1781913263, 411774}},      // cos(pi/2^14), then sin(pi/2^14)
  {{280022432, 2147483638}, {892988659, 205887}},        // cos(pi/2^15), then sin(pi/2^15)
  {{1143747429, 2147483645}, {1520490156, 102943}},      // cos(pi/2^16), then sin(pi/2^16)
};

static struct sCosSin cossin[4 << (POWERS_2 - 2)];
static double Cosine[5 * QUARTER_CIRCLE + 1];
static complex firstFactor[MAX_FFT_LEN];
static complex secondFactor[MAX_FFT_LEN];
static complex transf[MAX_FFT_LEN];
static complex product[MAX_FFT_LEN];
static complex tempFFT[MAX_FFT_LEN];
static complex MontgomeryMultNTransf[MAX_FFT_LEN];
static complex TestNbrTransf[MAX_FFT_LEN];
// Use formulas sin(A+B) = sin A cos B + cos A sin B
// and cos(A+B) = cos A cos B - sin A sin B
static void initCosinesArray(void)
{
  struct sCosSin *ptrCosSin, *ptrOldCosSin, *ptrCosSinDelta;
  double invLimb = 1 / (double)LIMB_RANGE;
  double invSqLimb = invLimb * invLimb;
  int index;
  cossin[0].Cos[0] = MAX_VALUE_LIMB;                       // cos(0) = 1
  cossin[0].Cos[1] = MAX_VALUE_LIMB;
  cossin[0].Sin[0] = 0;                                    // sin(0) = 0
  cossin[0].Sin[1] = 0;
  ptrCosSin = &cossin[1];
  for (index=1; ; index++)
  {
    // Get order of least significant non-zero bit.
    int bitNbr;
    int mask = 1;
    for (bitNbr = 0; ; bitNbr++)
    {
      if (index & mask)
      {
        break;
      }
      mask *= 2;
    }
    if (bitNbr == POWERS_2 - 2)
    {
      break;
    }
    ptrCosSinDelta = &cossinPowerOneHalf[(POWERS_2 - 3 - bitNbr)];  // Pointer to cos/sin B.
    if (index == mask)
    {
      ptrCosSin->Cos[0] = ptrCosSinDelta->Cos[0];
      ptrCosSin->Cos[1] = ptrCosSinDelta->Cos[1];
      ptrCosSin->Sin[0] = ptrCosSinDelta->Sin[0];
      ptrCosSin->Sin[1] = ptrCosSinDelta->Sin[1];
    }
    else
    {
      int firstProd[6], secondProd[6];
      // Compute cos(A+B) = cos A cos B - sin A sin B.
      ptrOldCosSin = ptrCosSin - mask;   // Pointer to cos/sin A.
      MultBigNbrComplete(ptrOldCosSin->Cos, ptrCosSinDelta->Cos, firstProd, 2);
      MultBigNbrComplete(ptrOldCosSin->Sin, ptrCosSinDelta->Sin, secondProd, 2);
      SubtractBigNbr(firstProd, secondProd, firstProd, 4);
      ptrCosSin->Cos[0] = *(firstProd + 2);
      ptrCosSin->Cos[1] = *(firstProd + 3);
      // Compute sin(A+B) = sin A cos B + cos A sin B.
      MultBigNbrComplete(ptrOldCosSin->Sin, ptrCosSinDelta->Cos, firstProd, 2);
      MultBigNbrComplete(ptrOldCosSin->Cos, ptrCosSinDelta->Sin, secondProd, 2);
      AddBigNbr(firstProd, secondProd, firstProd, 4);
      ptrCosSin->Sin[0] = *(firstProd + 2);
      ptrCosSin->Sin[1] = *(firstProd + 3);
    }
    ptrCosSin++;
  }
  // Convert from integers to doubles and send the results to the final array.
  ptrCosSin = cossin;
  for (index = 0; index < QUARTER_CIRCLE; index++)
  {
    double cosine = (double)ptrCosSin->Cos[0] * invSqLimb + (double)ptrCosSin->Cos[1] * invLimb;
    Cosine[index] = cosine;
    Cosine[HALF_CIRCLE - index] = -cosine;
    Cosine[HALF_CIRCLE + index] = -cosine;
    Cosine[2 * HALF_CIRCLE - index] = cosine;
    Cosine[2 * HALF_CIRCLE + index] = cosine;
    ptrCosSin++;
  }
  Cosine[QUARTER_CIRCLE] = 0;
  Cosine[3*QUARTER_CIRCLE] = 0;
}
/*
  Algorithm 9.5.6 of Crandall and Pomerance book Prime Numbers:
  X, Y: Pointers to complex numbers.

  J = 1; X = x; Y = y;
  for (d >= i > 0)
  {
    m = 0;
    while (m < D/2)
    {
      a = exp(-2*pi*i*m/D);
      for (J >= j > 0)
      {
        Y[0] = X[0] + X[D/2];
        Y[J] = a(X[0] - X[D/2]);
        X = X + 1;
        Y = Y + 1;
      }
      Y = Y + J;
      m = m + J;
    }
    J = 2 * J;
    X = X - D/2;
    Y = Y - D;
    (X,Y) = (Y,X);
  }
  if (d even) return complex data at X.
  return complex data at Y.
*/ 

// length is power of 2.
static void complexFFT(complex *x, complex *y, int length)
{
  int j, J;
  int halfLength = length / 2;
  int step = (1 << POWERS_2) / length;
  int exponentOdd = 0;
  complex *ptrX = x;
  complex *ptrY = y;
  complex *ptrZ;
  complex *ptrTemp;
  int angle;
  if (Cosine[0] == 0)
  {    // Cosines array not initialized yet. Initialize array.
    initCosinesArray();
  }
  ptrZ = ptrX + halfLength;
  for (angle = 0; angle < HALF_CIRCLE; angle += step)
  {
    double rootReal = Cosine[angle];
    double rootImag = Cosine[angle + QUARTER_CIRCLE];
    double tempReal = ptrX->real;
    double tempImag = ptrX->imaginary;
    double Zreal = ptrZ->real;
    double Zimag = ptrZ->imaginary;
    ptrY->real = tempReal + Zreal;
    ptrY->imaginary = tempImag + Zimag;
    tempReal -= Zreal;
    tempImag -= Zimag;
    ptrY++;
    ptrY->real = rootReal * tempReal - rootImag * tempImag;
    ptrY->imaginary = rootReal * tempImag + rootImag * tempReal;
    ptrX++;
    ptrY++;
    ptrZ++;
  }
  for (J = 2; J < length; J *= 2)
  {
    step *= 2;
    ptrTemp = ptrX - halfLength;
    ptrX = ptrY - length;
    ptrY = ptrTemp;
    ptrZ = ptrX + halfLength;
    exponentOdd = 1 - exponentOdd;
    for (angle = 0; angle < HALF_CIRCLE; angle += step)
    {
      double rootReal = Cosine[angle];
      double rootImag = Cosine[angle + QUARTER_CIRCLE];
      complex *ptrW = ptrY + J;
      for (j = J; j > 0; j--)
      {
        double tempReal = ptrX->real;
        double tempImag = ptrX->imaginary;
        double Zreal = ptrZ->real;
        double Zimag = ptrZ->imaginary;
        ptrY->real = tempReal + Zreal;
        ptrY->imaginary = tempImag + Zimag;
        tempReal -= Zreal;
        tempImag -= Zimag;
        ptrW->real = rootReal * tempReal - rootImag * tempImag;
        ptrW->imaginary = rootReal * tempImag + rootImag * tempReal;
        ptrX++;
        ptrY++;
        ptrZ++;
        ptrW++;
      }
      ptrY += J;
    }
  }
  if (exponentOdd)
  {     // Move data from x to y.
    memcpy(y, x, length * sizeof(complex));
  }
}

// Formulas to use:
// Gr(k) = Xr(k)Ar(k) � Xi(k)Ai(k) + Xr(N/2�k)Br(k) + Xi(N/2�k)Bi(k)
// Gi(k) = Xi(k)Ar(k) + Xr(k)Ai(k) + Xr(N/2�k)Bi(k) � Xi(N/2�k)Br(k)
// for k = 0, 1, ..., N/2�1 and X(N/2) = X(0)
// Ar(k) = 1 � sin( PI k / N)
// Ai(k) = �cos( PI k / N)
// Br(k) = 1 + sin( PI k / N)
// Bi(k) = cos( PI k / N)
static void ConvertHalfToFullSizeFFT(complex *halfSizeFFT, complex *fullSizeFFT, int power2)
{
  int k;
  int step = (1 << (POWERS_2-1)) / power2;
  complex *ptrFullSizeFFT = fullSizeFFT;
  complex *ptrHalfSizeFFT = halfSizeFFT;
  complex *ptrHalfSizeFFTRev = halfSizeFFT + power2;
  ptrHalfSizeFFTRev->real = halfSizeFFT->real;
  ptrHalfSizeFFTRev->imaginary = halfSizeFFT->imaginary;
  for (k = 0; k < power2; k++)
  {
    int angle = k * step;
    double diffReal = ptrHalfSizeFFT->real - ptrHalfSizeFFTRev->real;
    double sumImag = ptrHalfSizeFFT->imaginary + ptrHalfSizeFFTRev->imaginary;
    double negativeSine = Cosine[angle + QUARTER_CIRCLE];
    double cosine = Cosine[angle];
    ptrFullSizeFFT->real = ptrHalfSizeFFT->real + ptrHalfSizeFFTRev->real +
      diffReal*negativeSine +
      sumImag*cosine;
    ptrFullSizeFFT->imaginary = ptrHalfSizeFFT->imaginary - ptrHalfSizeFFTRev->imaginary +
      sumImag*negativeSine -
      diffReal*cosine;
    ptrHalfSizeFFT++;
    ptrHalfSizeFFTRev--;
    ptrFullSizeFFT++;
  }
  ptrFullSizeFFT->real = 2*(halfSizeFFT->real - halfSizeFFT->imaginary);
  ptrFullSizeFFT->imaginary = 0;
}

// Formulas to use:
// Xr(k) = Gr(k)IAr(k) � Gi(k)IAi(k) + Gr(N/2�k)IBr(k) + Gi(N/2�k)IBi(k)
// Xi(k) = Gi(k)IAr(k) + Gr(k)IAi(k) + Gr(N/2�k)IBi(k) � Gi(N/2�k)IBr(k)
// for k = 0, 1, ..., N/2�1
// IAr(k) = 1 � sin( PI k / N)
// IAi(k) = cos( PI k / N)
// IBr(k) = 1 + sin( PI k / N)
// IBi(k) = -cos( PI k / N)
static void ConvertFullToHalfSizeFFT(complex *fullSizeFFT, complex *halfSizeFFT, int power2)
{
  int k;
  int step = (1 << (POWERS_2 - 1)) / power2;
  complex *ptrFullSizeFFT = fullSizeFFT;
  complex *ptrFullSizeFFTRev = fullSizeFFT + power2;
  complex *ptrHalfSizeFFT = halfSizeFFT;
  complex *ptrHalfSizeFFTRev = halfSizeFFT + power2;
  for (k = 0; k < power2; k++)
  {
    int angle = k * step;
    double diffReal = ptrFullSizeFFT->real - ptrFullSizeFFTRev->real;
    double sumImag = ptrFullSizeFFT->imaginary + ptrFullSizeFFTRev->imaginary;
    double negativeSine = Cosine[angle + QUARTER_CIRCLE];
    double cosine = Cosine[angle];
    ptrHalfSizeFFT->real = ptrFullSizeFFT->real + ptrFullSizeFFTRev->real +
      diffReal*negativeSine -
      sumImag*cosine;
    // Negative sign for imaginary part required for inverse FFT.
    ptrHalfSizeFFT->imaginary = -(ptrFullSizeFFT->imaginary - ptrFullSizeFFTRev->imaginary +
      sumImag*negativeSine +
      diffReal*cosine);
    ptrHalfSizeFFT++;
    ptrHalfSizeFFTRev--;
    ptrFullSizeFFT++;
    ptrFullSizeFFTRev--;
  }
}

static int ReduceLimbs(limb *factor, complex *fftFactor, int len)
{
  int bitExternal = 0;  // Least significant bit of current external limb that corresponds to
                        // bit zero of FFT internal limb.
  limb *ptrFactor = factor;
  complex *ptrInternalFactor = fftFactor;
  for (;;)
  {
    int real = ptrFactor->x >> bitExternal;
    if (ptrFactor - factor < len - 1)
    {                   // Do not read outside input buffer.
      real += ((ptrFactor + 1)->x << (BITS_PER_GROUP - bitExternal));
    }
    ptrInternalFactor->real = (double)(real & MAX_VALUE_FFT_LIMB);
bitExternal += FFT_LIMB_SIZE;
if (bitExternal >= BITS_PER_GROUP)
{                   // All bits of input limb have been used.
  bitExternal -= BITS_PER_GROUP;
  if (++ptrFactor - factor == len)
  {
    ptrInternalFactor++->imaginary = 0;
    break;
  }
}
int imaginary = ptrFactor->x >> bitExternal;
if (ptrFactor - factor < len - 1)
{                   // Do not read outside input buffer.
  imaginary += (ptrFactor + 1)->x << (BITS_PER_GROUP - bitExternal);
}
ptrInternalFactor++->imaginary = (double)(imaginary & MAX_VALUE_FFT_LIMB);
bitExternal += FFT_LIMB_SIZE;
if (bitExternal >= BITS_PER_GROUP)
{                   // All bits of input limb have been used.
  bitExternal -= BITS_PER_GROUP;
  if (++ptrFactor - factor == len)
  {
    break;
  }
}
  }
  return (int)(ptrInternalFactor - fftFactor);
}

/*
   Algorithm 9.5.12 of Crandall and Pomerance book Prime Numbers:

   Zero-pad x and y until each has length 2D.
   X = DFT(x);
   Y = DFT(y);
   Z = X * Y;      // Using convolution
   z = DFT^(-1)(Z)
   z = round(z)    // Round elementwise
   carry = 0;
   for (0 <= n < 2D)
   {
     v = z_n + carry;
     z_n = v mod B
     carry = floor(v/B)
   }
   Delete leading zeros.
*/
void fftMultiplication(limb *factor1, limb *factor2, limb *result, int len, int *pResultLen)
{
  complex *ptrFirst, *ptrSecond, *ptrProduct;
  double invPower2;
  double dCarry;
  int fftLen, bitExternal;
  int power2plus1;
  limb *ptrResult;
  fftLen = ReduceLimbs(factor1, firstFactor, len);
  if (factor1 != factor2 && !(TestNbrCached == NBR_CACHED && factor2 == TestNbr) &&
    !(MontgomeryMultNCached == NBR_CACHED && factor2 == MontgomeryMultN))
  {
    ReduceLimbs(factor2, secondFactor, len);
  }
  // Get next power of 2 to len.
  int power2, index;
  for (power2 = 1; ; power2 *= 2)
  {
    if (power2 >= fftLen)
    {
      power2 += power2;
      break;
    }
  }
  for (index = fftLen; index < power2; index++)
  {
    firstFactor[index].real = 0;
    firstFactor[index].imaginary = 0;
    secondFactor[index].real = 0;
    secondFactor[index].imaginary = 0;
  }
  complexFFT(firstFactor, tempFFT, power2);
  ConvertHalfToFullSizeFFT(tempFFT, product, power2);   // product <- DFT(firstFactor)
  power2plus1 = power2 + 1;
  if (factor1 != factor2)
  {
    if (TestNbrCached == NBR_CACHED && factor2 == TestNbr)
    {
      memcpy(transf, TestNbrTransf, power2plus1 * sizeof(transf[0]));
    }
    else if (MontgomeryMultNCached == NBR_CACHED && factor2 == MontgomeryMultN)
    {
      memcpy(transf, MontgomeryMultNTransf, power2plus1 * sizeof(transf[0]));
    }
    else
    {
      complexFFT(secondFactor, tempFFT, power2);
      ConvertHalfToFullSizeFFT(tempFFT, transf, power2);  // transf <- DFT(secondFactor)
    }
    if (TestNbrCached == NBR_READY_TO_BE_CACHED && factor2 == TestNbr)
    {
      memcpy(TestNbrTransf, transf, power2plus1 * sizeof(transf[0]));
      TestNbrCached = NBR_CACHED;
    }
    else if (MontgomeryMultNCached == NBR_READY_TO_BE_CACHED && factor2 == MontgomeryMultN)
    {
      memcpy(MontgomeryMultNTransf, transf, power2plus1 * sizeof(transf[0]));
      MontgomeryMultNCached = NBR_CACHED;
    }
  }
  else
  {
    memcpy(transf, product, power2plus1 * sizeof(product[0]));   // transf <- DFT(secondFactor)
  }

    // Perform convolution.
  ptrFirst = product;
  ptrSecond = transf;
  ptrProduct = product;
  for (index = 0; index <= power2; index++)
  {
    double real = ptrFirst->real*ptrSecond->real - ptrFirst->imaginary*ptrSecond->imaginary;
    ptrProduct->imaginary = ptrFirst->real*ptrSecond->imaginary + ptrFirst->imaginary*ptrSecond->real;
    ptrProduct->real = real;
    ptrFirst++;
    ptrSecond++;
    ptrProduct++;
  }
  ConvertFullToHalfSizeFFT(product, tempFFT, power2);
  // Perform inverse DFT of product.
  complexFFT(tempFFT, transf, power2);
  ptrProduct = transf;
  invPower2 = (double)1 / ((double)(power2 * 8));
  dCarry = 0;
  memset(result, 0, 2*len * sizeof(limb));
  bitExternal = 0;
  ptrResult = result;
  for (index = 0; index < power2; index++)
  {
    double dQuot;
    int fftResult;

    // Real part.
    dCarry += floor(ptrProduct->real * invPower2 + 0.5);
    dQuot = floor(dCarry / (double)FFT_LIMB_RANGE);
    fftResult = (int)(dCarry - dQuot * (double)FFT_LIMB_RANGE);
    ptrResult->x |= (fftResult << bitExternal) & MAX_INT_NBR;
    if (bitExternal > BITS_PER_GROUP - FFT_LIMB_SIZE)
    {
      (ptrResult+1)->x |= (fftResult >> (BITS_PER_GROUP - bitExternal)) & MAX_INT_NBR;
    }
    bitExternal += FFT_LIMB_SIZE;
    if (bitExternal >= BITS_PER_GROUP)
    {
      bitExternal -= BITS_PER_GROUP;
      if (++ptrResult - result == 2 * len)
      {
        break;
      }
    }
    dCarry = dQuot;

    // Imaginary part. Use negative value for inverse FFT.
    dCarry += floor(-ptrProduct++->imaginary * invPower2 + 0.5);
    dQuot = floor(dCarry / (double)FFT_LIMB_RANGE);
    fftResult = (int)(dCarry - dQuot * (double)FFT_LIMB_RANGE);
    ptrResult->x |= (fftResult << bitExternal) & MAX_INT_NBR;
    if (bitExternal > BITS_PER_GROUP - FFT_LIMB_SIZE)
    {
      (ptrResult + 1)->x |= (fftResult >> (BITS_PER_GROUP - bitExternal)) & MAX_INT_NBR;
    }
    bitExternal += FFT_LIMB_SIZE;
    if (bitExternal >= BITS_PER_GROUP)
    {
      bitExternal -= BITS_PER_GROUP;
      if (++ptrResult - result == 2 * len)
      {
        break;
      }
    }
    dCarry = dQuot;
  }
  if (pResultLen != NULL)
  {
    if ((result + len - 1)->x == 0)
    {
      len--;
    }
    *pResultLen = len;
  }
}
