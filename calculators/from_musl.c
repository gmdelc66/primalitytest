/* Code from MUSL library */

#include <stdint.h>
#include <string.h>

union fi { double f; uint64_t i; };


int memcmp(const void *vl, const void *vr, size_t n)
{
	const unsigned char *l=(const unsigned char *)vl, *r=(const unsigned char *)vr;
	for (; n && *l == *r; n--, l++, r++);
	return n ? *l-*r : 0;
}

#ifdef __clang__
#define WT size_t
#define WS (sizeof(WT))
#endif

size_t strlen(const char *s)
{
  const char *a = s;
  while (*a)
  {
    a++;
  }
  return a - s;
}

double scalbn(double x, int n)
{
  union fi u;
  double y = x;

  u.i = (uint64_t)(0x3ff + n) << 52;
  x = y * u.f;
  return x;
}

/*
 * ====================================================
 * Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.
 *
 * Developed at SunSoft, a Sun Microsystems, Inc. business.
 * Permission to use, copy, modify, and distribute this
 * software is freely granted, provided that this notice
 * is preserved.
 * ====================================================
 */

static const double
ln2_hi = 6.93147180369123816490e-01,  /* 3fe62e42 fee00000 */
ln2_lo = 1.90821492927058770002e-10,  /* 3dea39ef 35793c76 */
Lg1 = 6.666666666666735130e-01,  /* 3FE55555 55555593 */
Lg2 = 3.999999999940941908e-01,  /* 3FD99999 9997FA04 */
Lg3 = 2.857142874366239149e-01,  /* 3FD24924 94229359 */
Lg4 = 2.222219843214978396e-01,  /* 3FCC71C5 1D8E78AF */
Lg5 = 1.818357216161805012e-01,  /* 3FC74664 96CB03DE */
Lg6 = 1.531383769920937332e-01,  /* 3FC39A09 D078C69F */
Lg7 = 1.479819860511658591e-01;  /* 3FC2F112 DF3E5244 */

double log(double x)
{
  union fi u;
  u.f = x;
	double hfsq,f,s,z,R,w,t1,t2,dk;
	uint32_t hx;
	int k;

	hx = u.i>>32;
	k = 0;

	/* reduce x into [sqrt(2)/2, sqrt(2)] */
	hx += 0x3ff00000 - 0x3fe6a09e;
	k += (int)(hx>>20) - 0x3ff;
	hx = (hx&0x000fffff) + 0x3fe6a09e;
	u.i = (uint64_t)hx<<32 | (u.i&0xffffffff);
	x = u.f;

	f = x - 1.0;
	hfsq = 0.5*f*f;
	s = f/(2.0+f);
	z = s*s;
	w = z*z;
	t1 = w*(Lg2+w*(Lg4+w*Lg6));
	t2 = z*(Lg1+w*(Lg3+w*(Lg5+w*Lg7)));
	R = t2 + t1;
	dk = k;
	return s*(hfsq+R) + dk*ln2_lo - hfsq + f + dk*ln2_hi;
}

static const double
half[2] = {0.5,-0.5},
ln2hi = 6.93147180369123816490e-01, /* 0x3fe62e42, 0xfee00000 */
ln2lo = 1.90821492927058770002e-10, /* 0x3dea39ef, 0x35793c76 */
invln2 = 1.44269504088896338700e+00, /* 0x3ff71547, 0x652b82fe */
P1   =  1.66666666666666019037e-01, /* 0x3FC55555, 0x5555553E */
P2   = -2.77777777770155933842e-03, /* 0xBF66C16C, 0x16BEBD93 */
P3   =  6.61375632143793436117e-05, /* 0x3F11566A, 0xAF25DE2C */
P4   = -1.65339022054652515390e-06, /* 0xBEBBBD41, 0xC5D26BF1 */
P5   =  4.13813679705723846039e-08; /* 0x3E663769, 0x72BEA4D0 */

double exp(double x)
{
	double hi, lo, c, xx, y;
	int k, sign;
	uint32_t hx;
  union fi __u;
  __u.f = x;
  hx = __u.i >> 32;
	sign = hx>>31;
	hx &= 0x7fffffff;  /* high word of |x| */

	/* argument reduction */
	if (hx > 0x3fd62e42) {  /* if |x| > 0.5 ln2 */
		if (hx >= 0x3ff0a2b2)  /* if |x| >= 1.5 ln2 */
			k = (int)(invln2*x + half[sign]);
		else
			k = 1 - sign - sign;
		hi = x - k*ln2hi;  /* k*ln2hi is exact here */
		lo = k*ln2lo;
		x = hi - lo;
	} else if (hx > 0x3e300000)  {  /* if |x| > 2**-28 */
		k = 0;
		hi = x;
		lo = 0;
	} else {
		/* inexact if x!=0 */
		return 1 + x;
	}

	/* x is now in primary range */
	xx = x*x;
	c = x - xx*(P1+xx*(P2+xx*(P3+xx*(P4+xx*P5))));
	y = 1 + (x*c/(2-c) - lo + hi);
	if (k == 0)
		return y;
	return scalbn(y, k);
}

double pow(double x, double y)
{
	return exp(y*log(x));
}
