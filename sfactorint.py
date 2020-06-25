""" To use this library, use:
    from sfactorint import p2ecm 

    To build ecm, from the primality test directory, simply do
    cd calculators
    make
    cd ..
    ipython3
    from sfactorint import p2ecm
"""

import math
import random
import re
from subprocess import Popen, PIPE


def powers(hm, y):
   return hm%y

""" Xploder iterates up a powers of two tree -1
"""

def Xploder(s, iter=1):
  return ((s+1) << (iter))-1


def primes_sieve2(limit):
    a = [True] * limit
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):
                a[n] = False  

def larsprimetest(hm):
   if hm == 1 or hm == 0:
      return False
   larstest = [-2, -1, 0, 1, 2]
   primereducer = list(primes_sieve2(hm.bit_length()))
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

"""
    I devised a method by tweaking the math for the Lucas Lehmer test and added looking for primes
    near the powers of two. This is the result of the work I did and it finds primes very well. I hope
    you enjoy it, it's actually not bad as a prime finder.
   
    Here is an example:
   
    In [198]: LLL(1009732533765211)
    Out[198]: 11344301
   
    And here are examples for the numbers at https://stackoverflow.com/questions/4078902/cracking-short-rsa-keys
   
    In [199]: LLL(10142789312725007)
    Out[199]: 100711423
   
    In [200]: LLL(8114231289041741)
    Out[200]: 1839221
"""

def LLL(N):
   p = 1<<N.bit_length()-1
   if N == 2:
     return 2
   if N == 3:
     return 3
   s = 4
   M = pow(p, 2) - 1
   for x in range (1, 100000):
     s = (((s * N ) - 2 )) % M
     xx = [math.gcd(s, N)] + [math.gcd(s*p+x,N) for x in range(7)] + [math.gcd(s*p-x,N) for x in range(1,7)] 
     try:
        prime = min(list(filter(lambda x: x not in set([1]),xx)))
     except:
        prime = 1
     if prime == 1:
        continue
     else:
        break
   #print (s, x, prime, xx)
   return prime

def ecm(N):
         try:
           process = Popen(["calculators/ecm", str(N)], stdout=PIPE)
         except:
           print()
           print()
           print("caclulators/ecm doesn't exist, the returned result wiil be incorrect")
           print("You can fix this by following the directions in the source or by:")
           print("cd calculators")
           print("make")
           print()
           print("This should create ecm and you'll be able to use sfactorint.")
           print("Currently this works under linux, OSX, termux android app and")
           print("other distributions.")
           print()
           print("The future version of this program will be moved to another repo:")
           print("sfactorint which will automatically compile Alpertons ecm so this")
           print("manual intervention is only temporary. I only included it because")
           print("i thought those that would take time to do the manual steps would")
           print("find it worth it to get access to Alpertons ECM factoring")
           return 0
         (output, err) = process.communicate()
         exit_code = process.wait()

         factors = output.decode().split('=')[1].split('<')[0].split('*')

         prevtemp = []
         for xx in factors:
           factorsstring = re.sub(r'\([^)]*\)', '',xx)
           multiple = factorsstring.find("^")
           if multiple > 0:
               answer = factorsstring[:multiple]
               repeat = factorsstring[multiple+1:]
               for x in range(int(repeat)):
                 prevtemp.append(int(answer))
           else:
              prevtemp.append(int(factorsstring.replace(' ', '')))
         return prevtemp

def p2ecm(N, withstatus=False):
   if withstatus == True:
     print(f"Attempting to factorise: {N}")
   b = num = N 
   vv = []
   lprime = False
   larstest = [-2, -1, 0, 1, 2]
   while larsprimetest(num) == False and num != 1:
     for x in larstest:
       b = get_factor_lars_prime(num, x)[0]
       if larsprimetest(b) == True:
         lprime = True
         break
     if larsprimetest(b) == False:
       factors = get_factors_lars_factorise(b)
       for xx in factors:
           num = num // xx
           vv.append(xx)
     else:
           num = num // b
           vv.append(b)
   if num != 1:
     if lprime == True:
       vv.append(num)
     elif lprime == False:
       vv.append(b)
   return vv

def get_factors_lars_factorise(hm, offset=-2, withstatus=False):
   num = hm
   vv = []
   while larsprimetest(num // 1) != True:
     if withstatus == True:
       print(vv, num)
     a = find_prime_evens_factorise(num, offset)
     if type(a[5]) == list:
        vv.extend(a[5])
        for xx in a[5]:
           num = num // xx
        break
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
     if withstatus == True:
       print(vv)
     num = num // vv[-1]
   if larsprimetest(num):
     vv.append(num)
   if withstatus == True:
     print(vv)
   return vv     

def get_factor_lars_prime(hm, offset=-2, withstatus=False):
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

def lars_find_prime(hm, offset=-2, withstatus=False):
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

def find_prime_evens_factorise(hm, offset=-2, withstatus=False):
  y = 3
  prevtemp = 3
  if larsprimetest(hm):
     if withstatus == True:
       print(f"{hm} is already prime")
     return hm
  while True:
    if y.bit_length() > hm.bit_length() -1:
      prevtemp = ecm(hm)
      break
    j = powers(hm, y)
    temp = j
    if j != 1 and j != 0:
      temp = j
      temp = hm % temp
      if temp == 0:
         prevtemp = temp
         if withstatus == True:
           print("c: break")
         break
      while temp != 1 and temp != 0:
         prevtemp = temp
         temp = hm % temp
    if temp == 0:
      if withstatus == True:
         print("h: break")
      break
    y = Xploder(y) -offset
  return hm, j, y.bit_length(), y, temp, prevtemp
