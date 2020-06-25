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


""" Fastest modulus reduction of powers of two which i discovered while studying primes. Other shortcuts may 
    exist i'm looking for them too to speed up my modulus reductions above. This is the same as doing the
    following:
    1008%512
    # 496
    496%256
    # 240
    240%128
    # 112
    112%64
    # 48
    48%32
    # 16
    16%16 
    # 0
    With lars_last_modulus_powers_of_two(1008) you will get the answer 16 immediately. This works for all numbers
    walking down a modulus powwers of two tree without having to walk down the tree.
    
    In [2601]: lars_last_modulus_powers_of_two(1008)                                                                                                
    Out[2601]: 16
"""

def lars_last_modulus_powers_of_two(hm):
   return math.gcd(hm, 1<<hm.bit_length())

""" pow_mod_p2() is much faster than pow() for numbers with a modulus of the powers of 2 

    Example speed increase:

    In [760]: import time   
     ...: start = time.time()   
     ...: pow_mod_p2(1009732533765251, sinn, 1<<((sinn.bit_length()-1)))  
     ...: end = time.time()   
     ...: print(end-start) 
     ...:                                                                                                                                                                                          
     1.6118049621582031

     In [761]: import time   
     ...: start = time.time()   
     ...: pow(1009732533765251, sinn, 1<<((sinn.bit_length()-1)))  
     ...: end = time.time()   
     ...: print(end-start)                                                                                                                                                                         

     5.584430932998657

     where sinn is a 4096 byte prime number.

"""

def pow_mod_p2(x, y, z):
    "Calculate (x ** y) % z efficiently."
    number = 1
    while y:
        if y & 1:
            number = modular_powerxz(number * x, z)
        y >>= 1
        x = modular_powerxz(x * x, z)
    return number

""" modular_powerxz is only for use for fast modulus of powers of 2 numbers, upto the offset of -2 to +2.
    It offers 4-5x speed faster than straight % mod or pow(x,y,z) where z is a modulus that is within
    the powers of 2 and an offset up to -2 to +2 away.
"""

def modular_powerxz(num, z, bitlength=1, offset=0):
   xpowers = 1<<(z.bit_length()-bitlength)
   if ((num+1) & (xpowers-1)) == 0:
      return num%xpowers
   elif offset == -2:
      return ( num & ( xpowers -bitlength)) + 2
   elif offset == -1:
      return ( num & ( xpowers -bitlength)) + 1
   elif offset == 0:
      return ( num & ( xpowers -bitlength))      
   elif offset == 1:
      return ( num & ( xpowers -bitlength)) - 1
   elif offset == 2:
      return ( num & ( xpowers -bitlength)) - 2

""" Here is a random powers of 2 prime finder. Instead of a traditional random number find and next_prime find, 
    It finds a random number that passes the lars_last_modulus_powers_of_two and checks if it's answer which is 
    (randomnum//2): pow(answer, 2 ** powersnumber-1, 2 ** powersnumber) passes an is prime test and continues until it
    finds a prime number as the answer.

   Here is an example if withstats is True:

   In [8376]: random_powers_of_2_prime_finder(500,withstats=True)                                                                                                         

   Out[8376]: 'pow(666262300770453383069409586449388105866418680981109533955324455061042093893855903254102021029841224158334524986498089277831523295501050122115012763111, 2**500-1, 2**500) = 896210381184287864297818969694142462892609158257898833237071849213575043971828530532195572986889116466526908364900915586299134290481831272303561385431'


    It returns an equation showing the prime result, here is another example:
    
    In [8436]: random_powers_of_2_prime_finder(100,withstats=True)                                                                                                         
    Out[8436]: 'pow(21228499098241391741518188355, 2**100-1, 2**100) = 648150045025216535003765994859'
 
    Notice the answer is an equation that finds a prime.
    
"""

def random_powers_of_2_prime_finder(powersnumber, primeanswer=False, withstats=True):
    while True:
       randnum = random.randrange((1<<(powersnumber-1))-1, (1<<powersnumber)-1,2)
       while lars_last_modulus_powers_of_two(randnum) == 2 and larsprimetest(randnum//2) == False:
         randnum = random.randrange((1<<(powersnumber-1))-1, (1<<powersnumber)-1,2)
       answer = randnum//2
       # This option makes the finding of a prime much longer, i would suggest not using it as 
       # the whole point is a prime answer. 
       if primeanswer == True:
          if larsprimetest(answer) == False:
            continue
       powers2find = pow_mod_p2(answer, (1<<powersnumber)-1, 1<<powersnumber)
       if larsprimetest(powers2find) == True:
          break
       else:  
          continue
    if withstats == False:
      return powers2find
    elif withstats == True:
      return f"pow_mod_p2({answer}, 2**{powersnumber}-1, 2**{powersnumber}) = {powers2find}"
    return powers2find
