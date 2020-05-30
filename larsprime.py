# This is a non probabilistic primality test. It preforms fermat's test from the bitlength of the number down to 2. 
# It then uses my algorithim to determine whether a number is composed of small primes. 
# If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
# is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
# works via algorithims which do not use randomness to reduce errors


#import numpy as np


def SieveOfEratosthenes(n):  
      
   # Create a boolean array "prime[0..n]" and initialize  
   #  all entries it as true. A value in prime[i] will  
   # finally be false if i is Not a prime, else true.  
   prime = [True for i in range(n+1)]  
   p = 2 
   while (p * p <= n):  
          
       # If prime[p] is not changed, then it is a prime  
       if (prime[p] == True):  
              
           # Update all multiples of p  
           for i in range(p * p, n+1, p):  
               prime[i] = False 
       p += 1 

   size = 0 
   for p in range(2, n+1):  
     if prime[p]: 
       size+=1 

   #vv = np.zeros(size, dtype='int64') 
   vv = []
   count = 0  
   # Print all prime numbers  
   for p in range(2, n+1):  
       if prime[p]:  
           #vv[count] = p  
           vv.append(p)
           count+=1 
   return vv 


def get_factor_lars_prime(hm, offset=-2):
     num = hm
     vv = []
     a = lars_find_prime(num, offset)
     if a[5] == 0:
       vv.append(a[1])
     elif a[5] != 0 and a[3] == hm:
       vv.append(a[3])
     elif a[5] == 2:
       if num % 2 == 0:
         vv.append(a[5])
       else:
         vv.append(a[3])
     elif a[5] == 3:
       if num % 2 == 0:
          vv.append(2)
       elif num % 3 == 0:
          vv.append(3)
       elif num % 5 == 0:
          vv.append(5)
       elif num % a[3] == 0:
          vv.append(a[3])
     else:
       vv.append(a[5])
     num = num // vv[-1]
     return vv

""" This module test for primality, it is the prime focus for this code. A factorization module that uses it can be
    found below
"""

def larsprimetest(hm):
   if hm == 1:
      return False
   larstest = [-2, -1, 0, 1, 2]
   primereducer = SieveOfEratosthenes(hm.bit_length())
   primetest = 0
   for x in primereducer[0:3]:
     if hm == int(x):   
        return True
   for x in list(reversed(primereducer)):
     if  pow(int(x),hm-1,hm)%hm != 1:   
        return False
   for x in larstest:
     if get_factor_lars_prime(hm, x)[0] == hm:
        primetest += 1
   if primetest == 5:
        return True
   else:
        return False
   return True


def Xploder(s, iter=1):
  return ((s+1) << (iter))-1


def powers(hm, y):
   return hm%y

def find_prime_evens(hm, offset=-2):
   y = 3
   prevtemp = 3
   if larsprimetest(hm):
      print(f"{hm} is already prime")
      return hm
   count = 0
   while True:
     count += 1
     if y.bit_length() > hm.bit_length() -1:
       hm = hm**2
     j = powers(hm, y)
     temp = j
     if j != 1 and j != 0:
       temp = j
       temp = hm % temp   
       if temp == 0:
          prevtemp = temp
          break   
       while temp != 1 and temp != 0:
          prevtemp = temp
          temp = hm % temp
     if temp == 0:
       print("h: break")
       break
     y = Xploder(y) -offset
   return hm, j, y.bit_length(), y, temp, prevtemp, count

def lars_find_prime(hm, offset=-2):
   y = 3
   prevtemp = 3 
   count = 0
   while True:
     count += 1
     j = powers(hm, y)
     temp = j
     if j != 1 and j != 0:
       temp = j
       temp = hm % temp   
       if temp == 0:
          prevtemp = temp
          break   
       while temp != 1 and temp != 0:
          prevtemp = temp
          temp = hm % temp
     if temp == 0:
       break
     y = Xploder(y) -offset
   return hm, j, y.bit_length(), y, temp, prevtemp, count


def build_prime_number(hm):
   si = 1
   for x in range(len(hm)):
     si = si * hm[x]
   return si

""" This module will find the next prime for any number input
"""

def lars_next_prime(hm):
   if hm == 1:
      return 2
   if hm == 2:
      return 3
   if hm % 2 == 0:
      hm = hm + 1
   hm += 2
   while larsprimetest(hm) == False:
      hm += 2
   return hm


""" This modulde can reduce any number into it's composites. It's a non
    prime factorization module provided for those interested in seeing 
    how numbers can be reduced to composite numbers only. Even prime 
    numbers
"""
def try_nonfactorization_mod(hm):
  vv = []
  num = hm
  cr = pow(num,1,1<<(num).bit_length()-1)
  while num > 1 and cr != 0:
    while cr != 0:
      prevcr = cr
      cr = num%cr     
    vv.append(prevcr)
    num = (num // prevcr) -1
    cr = num%(1<<(num).bit_length()-1)
  vv.append(num)
  return vv


""" The following module recreates the array created by
    try_nonfactorization_mod
"""
def build_composite_number(hm):
   si = hm[-1]
   for x in range(len(hm)-2, -1, -1):
      si = si * hm[x] + hm[x]
   return si


""" The following is a naive implementation of finding prime numbers based on the code above.
    It shows that all factors of a number can be found be squaring a number until they are all
    found. The problem is that these squares get big and unless a super fast modular reduction
    algorithim is found, it is slow to find the factors for big numbers. But at least it shows 
    the theory is sound, it's just the practability is not there since we don't have a fast modular
    reduction algorithm. This prints at each factor found and shows the div'd or squared number it used
    to find the prime factor. It is for educational purposes for how my method works. There are much faster
    factorization algorithms that don't rely on modular reduction, for one of the fastest, check out:
    https://www.alpertron.com.ar/ECM.HTM
"""

def get_factors(hm, offset=-1):
   num = hm
   vv = []
   while larsprimetest(num // 1) != True:
     print(vv, num)
     a = find_prime_evens(num, offset)
     print(a)
     if a[5] == 0:
       vv.append(a[1])
     elif a[5] == 2:
       if num % 2 == 0:
         vv.append(a[5])
       else:
         vv.append(a[3])
     elif a[5] == 3:
       if num % 2 == 0:
          vv.append(2)
       elif num % 3 == 0:
          vv.append(3)
       elif num % 5 == 0:
          vv.append(5)
       elif num % a[3] == 0:
          vv.append(a[3])
     else:
       vv.append(a[5])
     print(a)
     num = num // vv[-1]
   if larsprimetest(num):
     vv.append(num)
   print(vv)
   return vv
