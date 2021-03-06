# This is a non probabilistic primality test. It preforms fermat's test from the bitlength of the number down to 2. 
# It then uses my algorithim to determine whether a number is composed of small primes. 
# If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
# is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
# works via algorithims which do not use randomness to reduce errors. I created a super fast modulus reduction
# technique that doesn't have to walk the entire mod path down from a powers of a 2 and am looking to create the
# same for other modulus reductions. I'm hoping other mathematicians will be interested and will do the same
# it would greatly increase the speed of the method i use. The reduction i created is lars_last_modulus_powers_of_two()


import math
import random
import re
import sys
from subprocess import Popen, PIPE

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

""" This module tests for primality, it is the prime focus for this code. A factorization module that uses it can be
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


""" This is a non probalistic version of the miller rabin test. It uses Seives up to the bitlength of the number
    and (m) div'd by the last modulus of it's powers of two.
"""
def primality_test_miller_rabin_non_random(a):
    m = a - 1
    lb = lars_last_modulus_powers_of_two(m)
    m = (m // lb )
    if a == 2:
      return True
    primereducer = SieveOfEratosthenes(a.bit_length()) 
    for x in list(reversed(primereducer)):  
        b = x   # random.randint(2, a - 1)
        j = 0
        z = pow(b, m, a)
        while not ((j == 0 and z == 1) or z == a - 1):
            if (j > 0 and z == 1 or j + 1 == lb):
                return False
            j += 1
            z = (z * z) % a

    return True

""" Xploder iterates up a powers of two tree -1
"""

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


""" Fuzzy factor was designed for finding psuedoprimes near powers of 2 numbers that can be reduced faster than a 
   straight factorization using many differerent algotihims. For example, Try: fuzzy_factor(2**1200-1, True) and 
   you get an almost instantaneous result with only 3 numbers that are False (psuedoprime). You can plug these numbers
   into PARI  and they can factor the numbers faster than you can by using PARI or factorint to reduce just the
   2**1200-1 itself.  PARI can't seem to factor 2**1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2**1200-1.
   
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number. fuzzy_factor was designed for 2**numbers-1, and a newer version fuzzy_factor_any() will be introduced
   here shortly as I'm making daily updates.

   What is *AMAZING* about fuzzy_factor. https://pari.math.u-bordeaux.fr/gp.html cannot reduce 2**1000-1, but using 
   fuzzy_factor, you can take the psuedoprime components, plug them into ECM, and fully reduce 2*1000-1 in a few
   minutes, as fuzzy_factor reduces the number into psuedoprimes that can be reduced further by ECM instead of a
   straight factorization of 2**1000-1. Use fuzzy_factor(2**1000-1, True) to get results back with whether the
   number is prime (True) or psuedoprime (False). You can then plug the False numbers into ECM to reduce the number
   into all of its factors. The default is False so you can use with build_prime_number() to build the original number 
   from the fuzzy factors. You can also try this with 2**500-1 and other numbers to see it's usefulness in combination
   with other factorization engines.

"""
def fuzzy_factor(hm, returnwithpsuedoprimeresults=False):
   b = num = hm
   vv = []
   lprime = False
   larstest = [-2, -1, 0, 1, 2]
   while larsprimetest(num) == False and num != 1:
     for x in larstest:
       b = get_factor_lars_prime(num, x)[0]
       if larsprimetest(b) == True:
         lprime = True
         break
     if returnwithpsuedoprimeresults == False:
        vv.append(b)
     elif returnwithpsuedoprimeresults == True:
        vv.append((b, larsprimetest(b)))
     num = num // b
   if num != 1:
     if lprime == True:
       if returnwithpsuedoprimeresults == False:
          vv.append(num)
       elif returnwithpsuedoprimeresults == True:
          vv.append((num, larsprimetest(num))) 
     elif lprime == False:
       if returnwithpsuedoprimeresults == False:
          vv.append(b)
       elif returnwithpsuedoprimeresults == True:
          vv.append((b, larsprimetest(b))) 
   print(vv)
   return vv

""" This is the fastest way to get the last modulus instead of modding down an entire powers of two tree.
    The only algorithims i've seen to do this actually walk down the tree. I found a shortcut and would 
    urge other mathematicians to look at this and see if they can come up with a shortcut for other fast
    modulus reduction routines. This is the fastest modulus reduction routine know to mankind that utilizes
    a gcd trick. Use build_composite_number(vv) to rebuild your number after building the path down to
    rebuild your number. For example:
    In [2600]: build_composite_number(powers_factorization_quantum_leap(525672532516910347814982256648))                                             
    Out[2600]: 525672532516910347814982256648
    
    build_composite_number is included in this library. Just use:
    from larsprime import * 
    to use it.
"""

def powers_nonfactorization_quantum_leap(hm):
  num=hm
  vv = []
  while num > 2:
    prevcr = (1<<(num.bit_length()))
    numgcd = math.gcd(num,prevcr)
    num = (num // numgcd) -1
    vv.append(numgcd)
  if num != 0:
    vv.append(num)
  return vv


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


""" Fuzzy factor was designed for finding psuedoprimes near powers of 2 numbers that can be reduced faster than a 
   straight factorization using many differerent algotihims. For example, Try: fuzzy_factor(2**1200-1, True) and 
   you get an almost instantaneous result with only 3 numbers that are False (psuedoprime). You can plug these numbers
   into PARI or ECM and they can factor the numbers faster than you can by using PARI and ECM to reduce just the
   2**1200-1 itself.  PARI can't seem to factor 2**1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2**1200-1.
    
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number.
   What is *AMAZING* about fuzzy_factor. https://pari.math.u-bordeaux.fr/gp.html cannot reduce 2**1000-1, but using 
   fuzzy_factor, you can take the psuedoprime components, plug them into ECM, and fully reduce 2*1000-1 in a few
   minutes, as fuzzy_factor reduces the number into psuedoprimes that can be reduced further by ECM instead of a
   straight factorization of 2**1000-1. Use fuzzy_factor(2**1000-1, True) to get results back with whether the
   number is prime (True) or psuedoprime (False). You can then plug the False numbers into ECM to reduce the number
   into all of its factors. The default is False so you can use with build_prime_number() to build the original number 
   from the fuzzy factors. You can also try this with 2**500-1 and other numbers to see it's usefulness in combination
   with other factorization engines.

   Here is an example output, try this with your favorite factorization engine in comparison to this usage:

   In [5]: build_prime_number(fuzzy_factorp2(2**1200-1))                                                                                                                  
   Out[5]:
17218479456385750618067377696052635483579924745448689921733236816400740691241745619397484537236046173286370919031961587788584927290816661024991609882728717344659503471655990880884679896520055123906467064419056526231345685268240569209892573766037966584735183775739433978714578587782701380797240772477647874555986712746271362892227516205318914435913511141036261375

   fuzzy_factorp2(2**1200-1,True) 

   Out[2606]: 
[(3, True),
 (3, True),
 (5, True),
 (7, True),
 (13, True),
 (5, True),
 (5, True),
 (31, True),
 (11, True),
 (41, True),
 (17, True),
 (257, True),
 (151, True),
 (251, True),
 (1601, True),
 (101, True),
 (401, True),
 (331, True),
 (61, True),
 (97, True),
 (241, True),
 (4051, True),
 (1201, True),
 (8101, True),
 (673, True),
 (1801, True),
 (601, True),
 (61681, True),
 (4801, True),
 (1321, True),
 (340801, True),
 (63901, True),
 (25601, True),
 (55201, True),
 (268501, True),
 (100801, True),
 (10567201, True),
 (4278255361, True),
 (4562284561, True),
 (1133836730401, True),
 (8846144025137201, False),
 (18518800563924107521, False),
 (13334701, True),
 (1182468601, True),
 (35657512630090883498190108804189845169601, False),
 (1461503031127477825099979369543473122548042956801, True),
 (8059720126266442627050052102446681278605043839701907629253987599434464819580116421853601,
  True)]

  You can than then use ECM or PARI to further reduce the False (psuedoprimes) to their factors faster than 
  current straight PARI or factorint factorizations of 2**1200-1.

"""

def fuzzy_factorp2(hm, returnwithpsuedoprimeresults=False):
   b = num = hm
   vv = []
   lprime = False
   larstest = [-2, -1, 0, 1, 2]
   while larsprimetest(num) == False and num != 1:
     for x in larstest:
       b = get_factor_lars_prime(num, x)[0]
       if larsprimetest(b) == True:
         lprime = True
         break
     if returnwithpsuedoprimeresults == False:
        vv.append(b)
     elif returnwithpsuedoprimeresults == True:
        vv.append((b, larsprimetest(b)))
     num = num // b
   if num != 1:
     if lprime == True:
       if returnwithpsuedoprimeresults == False:
          vv.append(num)
       elif returnwithpsuedoprimeresults == True:
          vv.append((num, larsprimetest(num))) 
     elif lprime == False:
       if returnwithpsuedoprimeresults == False:
          vv.append(b)
       elif returnwithpsuedoprimeresults == True:
          vv.append((b, larsprimetest(b))) 
   #print(vv)
   return vv


""" This fuzzy factor factorizes more than the fuzzy_factor. In doing so it's slower but time constrained so it 
    shouldn't take more than 5-10 minutes on any factor given and faster than that on smaller numbers. It has two
    forms of use, one is fuzzy_factor_time_constrained(100983434321342423242314234234242432) and the other is
    fuzzy_factor_time_constrained(100983434321342423242314234234242432, True) so you can see which answers are 
    psuedoprime

   In [614]: fuzzy_factor_time_constrained(100983434321342423242314234234242432, True)                                                                                    
   Out[614]: 
   [(2, True),
   (2, True),
   (2, True),
   (2, True),
   (2, True),
   (2, True),
   (2, True),
   (31, True),
   (7, False),
   (31, True),
   (74363, True),
   (80111, True),
   (19686553169943826729, False)]

   For powers of two -1 use fuzzy_factorp2. It is much, much faster.

"""

def fuzzy_factor_time_constrained(hm, returnwithpsuedoprimeresults=False):
   num = hm
   vv = []
   if larsprimetest(hm):
      return f"{hm} is already prime"
   larstest = [-2, -1, 0, 1, 2]
   while larsprimetest(num) == False and num != 1:
     for x in larstest:
       b = get_factor_lars_prime2(num, x)[0]
       #print(b)
       if larsprimetest(b) == True:
         break
     if returnwithpsuedoprimeresults == False:
        vv.append(b)
     elif returnwithpsuedoprimeresults == True:
        vv.append((b, larsprimetest(b)))
     num = num // b
     if larsprimetest(num):
        break
   if larsprimetest(num):
     if returnwithpsuedoprimeresults == False:
        vv.append(num)
     elif returnwithpsuedoprimeresults == True:
        vv.append((num, larsprimetest(b))) 
   elif num != 1:
     if returnwithpsuedoprimeresults == False:
        vv.append(b)
     elif returnwithpsuedoprimeresults == True:
        vv.append((b, larsprimetest(b))) 
   return vv

""" These modules are utilized by fuzzy factors """

def find_prime_evens2(hm, offset=-1):
   y = 3
   prevtemp = 3
   newtemp = 0
   orighm = hm
   count = 0
   while True:
     if count > 3000:
       return lars_find_prime(orighm, offset)
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
       #print("h: break")
       break
     y = Xploder(y) -offset
     if count == 1:
        newtemp = hm
   return hm, j, y.bit_length(), y, temp, prevtemp, count

""" These modules are utilized by fuzzy factors """

def get_factor_lars_prime2(hm, offset=-1):
     num = hm
     vv = []
     a = find_prime_evens2(num, offset)
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

""" This primemaker is unique in the sense that it uses a feature of primes to find a prime probable random number.
    All prime numbers * 2 have a lars_last_modulus_powers_of_two() of 2. I search for a random number with this
    feature. You will never find a prime number that doesn't pass this test. I then div mod the number and use fermats 
    test. If an isprime test returns True, but the number * 2, using lars_last_modulus_powers_of_two() returns a 
    result other than two, then the number is not trully prime. I then use a fermat test and this test is *almost* 
    always the number one as is shown in the 2nd to last number in the result.  ( The second number is the  prime 
    number found, and the second to last number is the pow test count):  

    larsrandomprimemaker(2**10,2**20, withstats=True)
    [846574, 423287, True, 1, 2, 1, True]

    The third two last number, 2 in this case, is the iterations it took to find a number with this feature. Finally,
    Since fermats test can fail ( like with the number 341), we finally test with a primetest on the number, if it 
    passes, the algorithm has found a prime and we return that result for use.

    Usage:
      In [6834]: larsrandomprimemaker(2**100,2**150)                                                                                                                         
      Out[6834]: 541408456740197577823198243314039608874260987

"""


def larsrandomprimemaker(smallend, largeend, withstats=False):
   if smallend % 2 == 0:
      smallend = smallend - 1
   if largeend % 2 == 0:
      largeend = largeend - 1
   count = 0
   count2 = 0
   while True:
     powtest = False
     count += 1

     primetest = True
     num = random.randrange(smallend,largeend,2)
     while lars_last_modulus_powers_of_two(num-1) != 2 and (num//2) %2 == 1 and pow(2, ((num//2)-1), num//2) != 1:
        num = random.randrange(smallend,largeend,2)

     if  pow(2, ((num//2)-1), num//2) == 1:
        count2 += 1
        powtest = True
     
     if larsprimetest(num//2) == True and primetest == True:
        break
     else:
        continue
   if withstats == True:
      return [num, num//2, larsprimetest(num//2), lars_last_modulus_powers_of_two(num-1), count, count2, powtest]
   elif withstats == False:
      return num//2

""" START PROBABALISTIC USE FOR EDUCATIONAL PURPOSES ONLY """            

""" The following is probabalistic due to the ability to use mersenne numbers to generate primes that do not pass the test, but
    without using those, it has an uncanny accurary rate.
    I include it for educational purposes not practicle purposes, but i think you'll be suprised by it's ability to pass any isprime
    test, that dont use mersenne numbers to generate the prime. So don't use it for production because you can use mersenne numbers to
    generate primes that don't pass the test. Either way i include it here for educational purposes and it's uncanny ability to
    generate primes that were not generated from a mersenne number. I can include more information on that here if anyone
    is interested. I created a .txt file in this directory to show how i came up with the pow list. I simply couldn't find
    any numbers that didn't fail the test when compared to isprime from sympy other than the powlist. I thought that was
    interesting. If anyone finds a number that fails, let me know. I'd be interested in seeing what number in the pow list
    is missing since i ran a weeks long random test and another stress test in making that text file which only came up 
    with the numbers in the pow list i use here.
""" 

def fast_probabilistic_isprime(hm):
    powlist = [2,3,5,17,257,641,65537]
    if hm % 2 == 0:
      return False
    if hm < 2**50:
       #print("This is to only be used on numbers greater than 2**50")
       return "Unknown"
    if (hm+1 != 0) and (hm+1 & (hm) == 0):
       #print("fast_probabilistic_isprime cannot determine primes -1 off the powers of two")
       return "Unknown"
    if lars_last_modulus_powers_of_two(hm+hm) != 2:
       return False
    for xx in powlist:
      if pow(xx, hm-1, hm) != 1:
        return False
    return True

""" This uses the probabalistic fast isprime function to find the next prime. Do not use for production i include
    if here because it is very good at making primes, but you can use mersenne numbers to generate primes that don't pass
    the test. Either way i include it here for educational purposes only. 
"""

def fast_probabilistic_next_prime(hm):
   if hm < 2**50:
       return "This is to only be used on numbers greater than 2**50"
   if hm % 2 == 0:
      hm = hm + 1
   hm += 2
   while fast_probabilistic_isprime(hm) == False:
      hm += 2
   return hm

""" This creates a random number and then finds the next prime using he probabalistic fast isprime function. It's usage is:
    create_probabilistic_prime(1500). You must use a number greater than 50.  Do not use for production i include
    if here because it is very good at making primes, but you can use mersenne numbers to generate primes that don't pass
    the test. Either way i include it here for educational purposes only. 
"""

def create_probabilistic_prime(hm):
   if 2**hm < 2**50:
       return "This is to only be used on numbers greater than 2**50"
   num = random.randint(2**hm,2**(hm+1))
   return fast_probabilistic_next_prime(num)


""" This is a probabalistic primemaker based on using fast_probabalistic_isprime(). Do not use for production i include
    if here because it is very good at making primes, but you can use mersenne numbers to generate primes that don't pass
    the test. Either way i include it here for educational purposes only. 
"""

def larsprobabilisticprimemaker(smallend, largeend, withstats=False):
   if smallend < 2**50  or largeend <  2**50:
      return "This primemaker is only for use of primes larger than 2**50. Please Try a larger number"
   if smallend % 2 == 0:
      smallend = smallend - 1
   if largeend % 2 == 0:
      largeend = largeend - 1
   count = 0
   while True:
     primetest = True
     num = random.randrange(smallend,largeend,2)
     while fast_probabilistic_isprime(num//2) == False:
        num = random.randrange(smallend,largeend,2)
        count += 1
     break
   if withstats == True:
      return [num, num//2, lars_last_modulus_powers_of_two(num-1), count]
   elif withstats == False:
      return num//2

""" END PROBABALISTIC FOR EDUCATIONAL PURPOSES ONLY """            


""" Prime Sieve Maker found on the internet """

def primes_sieve2(limit):
    a = [True] * limit
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):
                a[n] = False            

""" powers_of_2_prime_maker() Here is it's description:
    Use any number here but use the sieves numbers here to see that only prime numbers can make prime numbers
    via pow(xx, 2**x-1, 2**x), where only those answers match up to other primes. It's like a 1 to 1 ratio.
    Where xx is a prime number and x is the iteration of the loop. For example:

    In [8128]: powers_of_2_prime_maker(6)                                                                                                                                     
    pow(53, 2**6-1, 2**6) = 29 and is Prime, 53 is Prime?: True, 2**6-1 is Prime?: False
    pow(43, 2**6-1, 2**6) = 3 and is Prime, 43 is Prime?: True, 2**6-1 is Prime?: False
    pow(31, 2**6-1, 2**6) = 31 and is Prime, 31 is Prime?: True, 2**6-1 is Prime?: False
    pow(29, 2**6-1, 2**6) = 53 and is Prime, 29 is Prime?: True, 2**6-1 is Prime?: False
    pow(13, 2**6-1, 2**6) = 5 and is Prime, 13 is Prime?: True, 2**6-1 is Prime?: False
    pow(5, 2**6-1, 2**6) = 13 and is Prime, 5 is Prime?: True, 2**6-1 is Prime?: False
    pow(3, 2**6-1, 2**6) = 43 and is Prime, 3 is Prime?: True, 2**6-1 is Prime?: False

    In [8129]: powers_of_2_prime_maker(7)                                                                                                                                      
    7: 127 already Prime
    pow(113, 2**7-1, 2**7) = 17 and is Prime, 113 is Prime?: True, 2**7-1 is Prime?: True
    pow(109, 2**7-1, 2**7) = 101 and is Prime, 109 is Prime?: True, 2**7-1 is Prime?: True
    pow(107, 2**7-1, 2**7) = 67 and is Prime, 107 is Prime?: True, 2**7-1 is Prime?: True
    pow(101, 2**7-1, 2**7) = 109 and is Prime, 101 is Prime?: True, 2**7-1 is Prime?: True
    pow(79, 2**7-1, 2**7) = 47 and is Prime, 79 is Prime?: True, 2**7-1 is Prime?: True
    pow(67, 2**7-1, 2**7) = 107 and is Prime, 67 is Prime?: True, 2**7-1 is Prime?: True
    pow(53, 2**7-1, 2**7) = 29 and is Prime, 53 is Prime?: True, 2**7-1 is Prime?: True
    pow(47, 2**7-1, 2**7) = 79 and is Prime, 47 is Prime?: True, 2**7-1 is Prime?: True
    pow(43, 2**7-1, 2**7) = 3 and is Prime, 43 is Prime?: True, 2**7-1 is Prime?: True
    pow(29, 2**7-1, 2**7) = 53 and is Prime, 29 is Prime?: True, 2**7-1 is Prime?: True
    pow(17, 2**7-1, 2**7) = 113 and is Prime, 17 is Prime?: True, 2**7-1 is Prime?: True
    pow(3, 2**7-1, 2**7) = 43 and is Prime, 3 is Prime?: True, 2**7-1 is Prime?: True


    Use https://www.mersenne.org/primes/  to find which primes are mersenne primes to test. Notice that in both
    cases the numbers generated show up as the first number in the pow() statement that generate a true prime,
    even if in the case of non mersenne numbers. I thought this was interesting so included it in this library.
    
    Notice that it seems that all numbers that end up as an answer are also seem to end up in the first pow(x,,)
    statement. This is what i mean by every prime in the series has it's answers in the series of primes used.

"""

def powers_of_2_prime_maker(x):
   primereducer = list(reversed(list(primes_sieve2(2**x-1))))
   if larsprimetest(2**x-1) == True:
      print(f"{x}: {2**x-1} already Prime")
   for xx in primereducer:
      if larsprimetest(pow(xx, 2**x-1, 2**x)) == True:
        print(f"pow({xx}, 2**{x}-1, 2**{x}) = {pow(xx, 2**x-1, 2**x)} and is Prime, {xx} is Prime?: {larsprimetest(xx)}, 2**{x}-1 is Prime?: {larsprimetest(2**x-1)}")

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


"""  This is a refactor of larsprimetest, i'm making the code more concise """

def larsisprime(hm, sieveiter=50):
   count = 0
   if hm == 1: return False
   if hm == 2: return True
   if lars_last_modulus_powers_of_two(hm+hm) != 2:
      return False
   primereducer = list(reversed(list(primes_sieve2(hm.bit_length()))))
   for x in list(reversed(primereducer)):
     if  pow(int(x),hm-1,hm) != 1:   
        return False
   gcdtest = larsgcd(hm)
   if gcdtest[2] == 1 or (gcdtest[1] == 0 and gcdtest[2] == hm):
      return True
   else:
      return False
   return True

""" larsgcd(num) returns any primes found within the offset of it's powers of two number.
    It doesn't find all primes, but does find many. Here are example usages (also showing
    that squaring a number can uncover it's primes). The third number is the prime unless
    the number is the number itself. In that case it's not used as a factor in larsisprime():

    In [939]: larsgcd(341)                                                                                                                                                                             
    Out[939]: (341, 0, 31)

    In [940]: larsgcd(101*1009)                                                                                                                                                                        
    Out[940]: (101909, 0, 101)
    
    In [941]: larsgcd(1009732533765203)                                                                                                                                                                
    Out[941]: (1009732533765203, 0, 1823)

    And squaring examples:

    In [942]: larsgcd((1009*1013)**2)                                                                                                                                                                   
    Out[942]: (1044723161689, 0, 1009)

    In [947]: larsgcd((1009*191)**2)                                                                                                                                                                   
    Out[947]: (37140612961, 0, 191)
    
""" 

def larsgcd(a, offset_range=[]):
  b = y = 3
  if a == 1: return 1, y, 0
  if a == 2 or a == 3 or a == 5: return 1, y, 1
  if a % 2 == 0: return a, y, 2
  if a % 3 == 0: return a, y, 3
  if a % 5 == 0: return a, y, 5
  for offset in [-2, -1, 0, 1, 2] + offset_range:
    b = y = 3
    while b < 1<<a.bit_length():
      prevy = y
      while b:
        prevb = b
        a,b = a, a%b
      if prevb != 1: 
        break
      y = Xploder(prevy) + offset
      b = y
  return a, b, prevb

""" get_factors_lars_opt is a combination of the routines above and a pollard brent optimization i made to
    increase it's speed. They must be used in conjunction as my optimization can cause pollard brent to find
    psuedoprimes at the lower boundry, so we use the tools i have included here to find the smaller primes. 

    This doesn't use the refactored larsgcd yet, as that's still in beta, but when its finished, this version
    should be much more compact and code consise.

    Example Usage:

    In [175]: get_factors_lars_opt(10097325337652014342342342342213)                                                                                                                                    
    [] 10097325337652014342342342342213
    h: break
    [19] 531438175665895491702228544327
    [19, 13523911] 39296189960573941347457
    [19, 13523911, 1372014439, 28641236450263]
    Out[175]: [19, 13523911, 1372014439, 28641236450263]

"""

def get_factors_lars_opt(hm, offset=-2):
   num = hm
   vv = []
   while larsprimetest(num // 1) != True:
     print(vv, num)
     a = find_prime_evens_lars_opt(num, offset)
     #print(a)
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
     #print(a)
     num = num // vv[-1]
   if larsprimetest(num):
     vv.append(num)
   print(vv)
   return vv


""" This is a standard pollard_brent with an optimization i made increase it's speed. It must be used in
    conjunction with the tools here to find all primes that it can
 """

def pollard_brent_lars_opt(n):
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    # This optimization is contributed by Lars Rocha. I use an equation instead of random numbers for significant
    # speed increases on larger numbers

    y,c,m = (1<<((n**2).bit_length()+1)), (1<<((n**2).bit_length())) , (1<<((n**2).bit_length()+1)) 

    #print(y,c,m)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g==1:
            ys = y
            for i in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x-y) % n
            g = math.gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = math.gcd(abs(x - ys), n)
            if g > 1:
                break

    return g


def find_prime_evens_lars_opt(hm, offset=-2): 
  y = 3 
  prevtemp = 3 
  if larsprimetest(hm): 
     print(f"{hm} is already prime") 
     return hm 
  while True: 
    if y.bit_length() > hm.bit_length() -1: 
      prevtemp = pollard_brent_lars_opt(hm) 
      break 
    j = powers(hm, y) 
    temp = j 
    if j != 1 and j != 0: 
      temp = j 
      temp = hm % temp    
      if temp == 0: 
         prevtemp = temp 
         print("c: break") 
         break    
      while temp != 1 and temp != 0: 
         prevtemp = temp 
         temp = hm % temp 
    if temp == 0: 
      print("h: break") 
      break 
    y = Xploder(y) -offset 
  return hm, j, y.bit_length(), y, temp, prevtemp 

""" fuzzy_factorp2_brent_pollard(num, returnwithpsuedoprimeresults=False)

    Use returnwithpsuedoprimeresults=True to see if any psuedoprimes are in the answer. Future versions should
    have these rather than the engine getting stuck on the factorization, but this is for a future release.

    This is in beta. It returns results for numbers that other prime engines can't 1 off the powers of 2. Maybe
    more but i haven't tested much yet. Try this with 2**600-1, 2**600+1, 2**700+1, 2**1200-1 And see that you 
    can get immediate results where with https://pari.math.u-bordeaux.fr/gp.html and 
    , sympy's factorint, cant seem to factor at all or near the speed this 
    can one off the powers of two. This is due to fuzzy_factor returning psuedoprimes that can be broken down 
    easier than the psuedoprimes those engines use.These are only a few numbers i tested, and as this is in beta, 
    i plan to enhane this further to return the psuedoprimes it get's stuck on until i implement better    
    factorization techniques. But for now, i can factor some numbers off the powers of 2 better than some of the 
    best engines using this simple method so i'm quite proud of that feat, and it will only get better as i 
    enhance the engine. Feel free to post on github any primes off the powers of 2 that other engines cant' do 
    but fuzzy_factorp2_brent_pollard can.  https://www.alpertron.com.ar/ECM.HTM can with about the same speed. It's
    really the best engine out there, but it's impressive i can match it's speed on some powers of two with just brent
    pollard.  Also you can use fuzzy_factorp2(num, returnwithpsuedoprimeresults=True) to get results fast as well.



    Here are the factors for 2**1200-1:

    print(fuzzy_factorp2_brent_pollard(2**1200-1))
    [3, 3, 5, 7, 13, 5, 5, 31, 11, 41, 17, 257, 151, 251, 1601, 101, 401, 331, 61, 97, 241, 4051, 1201, 8101, 
    673, 1801, 601, 61681, 4801, 1321, 340801, 63901, 25601, 55201, 268501, 100801, 10567201, 4278255361, 
    4562284561, 1133836730401, 2787601, 3173389601, 394783681, 46908728641, 13334701, 1182468601, 82471201, 
    432363203127002885506543172618401, 1461503031127477825099979369543473122548042956801, 
    8059720126266442627050052102446681278605043839701907629253987599434464819580116421853601]

    print(fuzzy_factorp2_brent_pollard(2**420+1))                                                                                                                            
    [17, 241, 61681, 4562284561, 15790321, 3361, 88959882481, 84179842077657862011867889681, 127681, 1130641,
     755667361, 54169520413224311136354324156824071681]

    print(fuzzy_factorp2_brent_pollard(2**600-1))                                                                                                                          
    [3, 3, 7, 5, 5, 5, 13, 31, 17, 61, 11, 151, 41, 241, 601, 101, 251, 331, 1321, 1801, 61681, 401, 1201, 4051, 
     8101, 63901, 340801, 268501, 100801, 10567201, 4562284561, 1133836730401, 2787601, 3173389601, 13334701, 
     1182468601, 1461503031127477825099979369543473122548042956801]

    print(fuzzy_factorp2_brent_pollard(2**600+1))                                                                                                                          
    [257, 97, 673, 1601, 4278255361, 4801, 25601, 55201, 394783681, 46908728641, 82471201, 
     432363203127002885506543172618401, 
     8059720126266442627050052102446681278605043839701907629253987599434464819580116421853601]

   Try these on your favorite engine too see if they can factor them with the speed here, if at all. Obviously
   those engines can factor faster than mine on numbers off the powers of 2 other than a few that i've found as
   i haven't implemented SIQS yet, but i thought this was interesting and wanted to share it since i only use 
   brent pollard and my engine to pull off this feat for the numbers above.

"""

def fuzzy_factorp2_brent_pollard(hm, returnwithpsuedoprimeresults=False):
   b = num = hm
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
       factors = get_factors_lars_prime_brent(b)
       for xx in factors:
           num = num // xx
           if returnwithpsuedoprimeresults == False:
             vv.append(xx)
           elif returnwithpsuedoprimeresults == True:
             vv.append((xx, larsprimetest(xx))) 
     else:
           num = num // b
           if returnwithpsuedoprimeresults == False:
              vv.append(b)
           elif returnwithpsuedoprimeresults == True:
              vv.append((b, larsprimetest(b))) 
     #if returnwithpsuedoprimeresults == False:
     #   vv.append(b)
     #elif returnwithpsuedoprimeresults == True:
     #   vv.append((b, larsprimetest(b)))
   if num != 1:
     if lprime == True:
       if returnwithpsuedoprimeresults == False:
          vv.append(num)
       elif returnwithpsuedoprimeresults == True:
          vv.append((num, larsprimetest(num))) 
     elif lprime == False:
       if returnwithpsuedoprimeresults == False:
          vv.append(b)
       elif returnwithpsuedoprimeresults == True:
          vv.append((b, larsprimetest(b))) 
   #print(vv)
   return vv

def get_factors_lars_prime_brent(hm, offset=-2):
   num = hm
   vv = []
   while larsprimetest(num // 1) != True:
     print(vv, num)
     a = find_prime_evens_lars_opt(num, offset)
     #print(a)
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
     #print(a)
     num = num // vv[-1]
   if larsprimetest(num):
     vv.append(num)
   print(vv)
   return vv
      
      
"""  fuzzy_factorp2_factorise utilizes the factorise.py siqs_factorise algorithim. With this utilization
     you can now factor faster and bigger numbrs than with sympy's factorint. If you use that library you
     may be very interested in trying this one out. I plan to make it faster and Here are some examples of 
     the factorization:

     fuzzy_factorp2_factorise(9843798475984375498379437897594953794798539278493345)                                                                                          
     [] 2170628109368109260943646724938247804806734129767
     Attempting POLLARD_BRENT
     POLLARD BRENT Success
     [5495639]
     [5495639] 394972833799328751568952532169279642423153
     Attempting POLLARD_BRENT
     Attempting factorise.py SIQS
     factorise.py SIQS Success
     [5495639, 146558421909808193, 2694985580851807826812721]
     Out[301]: [5, 907, 5495639, 146558421909808193, 2694985580851807826812721]

     In [291]: fuzzy_factorp2_factorise(984379847598437549837943789759495379479853927849334)                                                                                           
     [] 492189923799218774918971894879747689739926963924667
     Attempting POLLARD_BRENT
     POLLARD BRENT Success
     [62013403]
     [62013403] 7936831394323236460978796710765053318230689
     Attempting POLLARD_BRENT
     POLLARD BRENT Success
     [62013403, 487015843]
     [62013403, 487015843] 16296864893414230183429159430374123
     Attempting POLLARD_BRENT
     Attempting factorise.py SIQS
     factorise.py SIQS Success
     [62013403, 487015843, 294388349552734637, 55358389413759479]
     Out[291]: [2, 62013403, 487015843, 294388349552734637, 55358389413759479]

     You can utilize this rather than sympy's factorint if you looking for speed and factorizations it can't
     yet do. 

     In the future i plan to implment a faster SIQ's engine which should be faster so keep watching here for 
     updates.

     This update can reduce numbers less than 50 digits rather fast but is logrimically slow on larger numbers

     For exampele it an factor a 60 digit number like 632459103267572196107100983820469021721602147490918660274601  
     in about 30-45 minutes and factor a 41 digit number like 12785407097419647710079782477202050848441 in a few seconds.

"""

def fuzzy_factorp2_factorise(hm, returnwithpsuedoprimeresults=False):
   print(f"Attempting to factorise: {hm}")
   b = num = hm
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
           if returnwithpsuedoprimeresults == False:
             vv.append(xx)
           elif returnwithpsuedoprimeresults == True:
             vv.append((xx, larsprimetest(xx))) 
     else:
           num = num // b
           if returnwithpsuedoprimeresults == False:
              vv.append(b)
           elif returnwithpsuedoprimeresults == True:
              vv.append((b, larsprimetest(b))) 
     #if returnwithpsuedoprimeresults == False:
     #   vv.append(b)
     #elif returnwithpsuedoprimeresults == True:
     #   vv.append((b, larsprimetest(b)))
   if num != 1:
     if lprime == True:
       if returnwithpsuedoprimeresults == False:
          vv.append(num)
       elif returnwithpsuedoprimeresults == True:
          vv.append((num, larsprimetest(num))) 
     elif lprime == False:
       if returnwithpsuedoprimeresults == False:
          vv.append(b)
       elif returnwithpsuedoprimeresults == True:
          vv.append((b, larsprimetest(b))) 
   #print(vv)
   return vv

def get_factors_lars_factorise(hm, offset=-2):
   num = hm
   vv = []
   while larsprimetest(num // 1) != True:
     print(vv, num)
     a = find_prime_evens_factorise(num, offset)
     if type(a[5]) == list:
        vv.extend(a[5])
        for xx in a[5]:
           num = num // xx
        break
     #print(a)
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
     print(vv)
     num = num // vv[-1]
   if larsprimetest(num):
     vv.append(num)
   print(vv)
   return vv


def trial_division(hm):
    for xx in small_primes:
       if hm%xx == 0: return xx
    return hm

def find_prime_evens_factorise(hm, offset=-2):
  y = 3
  prevtemp = 3
  if larsprimetest(hm):
     print(f"{hm} is already prime")
     return hm
  while True:
    if y.bit_length() > hm.bit_length() -1:
      if len(str(hm)) < 17:
         print(f"Attempting  to factorise {hm} with trial division")
         prevtemp = trial_division(hm)
         if prevtemp != hm:
            print(f"Trial Division Success")
            break
         else:
           print(f"Attempting  to factorise {hm} with POLLARD_BRENT")
           while prevtemp != hm:
              prevtemp = pollard_brent_lars_opt(hm)
           print(f"POLLARD_BRENT Success")
      else:
         print(f"Attempting  to factorise {hm} with POLLARD_BRENT")
         prevtemp = pollard_brent_lars_opt(hm)
      if hm == prevtemp:
         print(f"Attempting to factorise {hm} with factorise.py SIQS")
         prevtemp = siqs_factorise(hm)
         print("factorise.py SIQS Success")
      else:
            print("POLLARD BRENT Success")
      break
    j = powers(hm, y)
    temp = j
    if j != 1 and j != 0:
      temp = j
      temp = hm % temp
      if temp == 0:
         prevtemp = temp
         print("c: break")
         break
      while temp != 1 and temp != 0:
         prevtemp = temp
         temp = hm % temp
    if temp == 0:
      print("h: break")
      break
    y = Xploder(y) -offset
  return hm, j, y.bit_length(), y, temp, prevtemp

def pollard_brent_lars_opt(n, limit=21):
  if n % 2 == 0: return 2
  if n % 3 == 0: return 3

  # This optimization is contributed by Lars Rocha. I use an equation instead of random numbers for significant
  # speed increases on larger numbers. Small numbers less than 16 in length require the random structure.
  length = len(str(n))
  if length > 16:
     y,c,m = (1<<((n**2).bit_length()+1)), (1<<((n**2).bit_length())) , (1<<((n**2).bit_length()+1))
  else:
     y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)

  #print(y,c,m)
  g, r, q = 1, 1, 1
  ii = 0
  while g == 1:
      x = y
      for i in range(r):
          y = (pow(y, 2, n) + c) % n
      k = 0
      while k < r and g==1:
          ys = y
          for i in range(min(m, r-k)):
              y = (pow(y, 2, n) + c) % n
              q = q * abs(x-y) % n
          g = math.gcd(q, n)
          k += m
      r *= 2
      if length > 16:
        ii += 1
        if ii > limit:
          return n
  if g == n:
      while True:
          ys = (pow(ys, 2, n) + c) % n
          g = math.gcd(abs(x - ys), n)
          if g > 1:
              break
  return g

""" from factorise.py instead of importing i include here as importing from the factorise.py library does not seem to work.
    I include the original factorise.py file in the repository unchanged for those interested in utilizing it. It can factor
    a 42 digit number in less than a minute and a 60 digit number in about an hour on a modest i7 4 core macbook.

    For exampele it an factor a 60 digit number like 632459103267572196107100983820469021721602147490918660274601  
    in about 30-45 minutes and factor a 41 digit number like 12785407097419647710079782477202050848441 in a few seconds.
"""
SIQS_TRIAL_DIVISION_EPS = 25
SIQS_MIN_PRIME_POLYNOMIAL = 400
SIQS_MAX_PRIME_POLYNOMIAL = 4000

class Polynomial:
    """A polynomial used for the Self-Initializing Quadratic Sieve."""

    def __init__(self, coeff=[], a=None, b=None):
        self.coeff = coeff
        self.a = a
        self.b = b

    def eval(self, x):
        res = 0
        for a in self.coeff[::-1]:
            res *= x
            res += a
        return res


class FactorBasePrime:
    """A factor base prime for the Self-Initializing Quadratic Sieve."""

    def __init__(self, p, tmem, lp):
        self.p = p
        self.soln1 = None
        self.soln2 = None
        self.tmem = tmem
        self.lp = lp
        self.ainv = None

small_primes = list(primes_sieve2(10000000))

def siqs_factorise(n):
    """Use the Self-Initializing Quadratic Sieve algorithm to identify
    one or more non-trivial factors of the given number n. Return the
    factors as a list.
    """
    dig = len(str(n))
    nf, m = siqs_choose_nf_m(dig)

    factor_base = siqs_factor_base_primes(n, nf)
    
    required_relations_ratio = 1.05
    success = False
    smooth_relations = []
    prev_cnt = 0
    i_poly = 0
    while not success:
        print("*** Step 1/2: Finding smooth relations ***")
        required_relations = round(len(factor_base) * required_relations_ratio)
        print("Target: %d relations at about 1 relation per second (sometimes faster) required" % required_relations)
        enough_relations = False
        while not enough_relations:
            if i_poly == 0:
                g, h, B = siqs_find_first_poly(n, m, factor_base)
            else:
                g, h = siqs_find_next_poly(n, factor_base, i_poly, g, B)
            i_poly += 1
            if i_poly >= 2 ** (len(B) - 1):
                i_poly = 0
            sieve_array = siqs_sieve(factor_base, m)
            enough_relations = siqs_trial_division(
                n, sieve_array, factor_base, smooth_relations,
                g, h, m, required_relations)

            if (len(smooth_relations) >= required_relations or
                i_poly % 8 == 0 and len(smooth_relations) > prev_cnt):
                #print("Total %d/%d relations." %
                #      (len(smooth_relations), required_relations))
                prev_cnt = len(smooth_relations)

        print("*** Step 2/2: Linear Algebra ***")
        print("Building matrix for linear algebra step...")
        M = siqs_build_matrix(factor_base, smooth_relations)
        M_opt, M_n, M_m = siqs_build_matrix_opt(M)

        print("Finding perfect squares using matrix...")
        perfect_squares = siqs_solve_matrix_opt(M_opt, M_n, M_m)

        print("Finding factors from perfect squares...")
        factors = siqs_find_factors(n, perfect_squares, smooth_relations)
        if len(factors) > 1:
            success = True
        else:
            print("Failed to find a solution. Finding more relations...")
            required_relations_ratio += 0.05

    return factors

#def siqs_choose_nf_m(d):
#    """Choose parameters nf (sieve of factor base) and m (for sieving
#    in [-m,m].
#    """
#    # Using similar parameters as msieve-1.52
#    if d <= 34:
#        return 200, 65536
#    if d <= 36:
#        return 300, 65536
#    if d <= 38:
#        return 400, 65536
#    if d <= 40:
#        return 500, 65536
#    if d <= 42:
#        return 600, 65536
#    if d <= 44:
#        return 700, 65536
#    if d <= 48:
#        return 1000, 65536
#    if d <= 52:
#        return 1200, 65536
#    if d <= 56:
#        return 2000, 65536 * 3
#    if d <= 60:
#        return 4000, 65536 * 3
#    if d <= 66:
#        return 6000, 65536 * 3
#    if d <= 74:
#        return 10000, 65536 * 3
#    if d <= 80:
#        return 30000, 65536 * 3
#    if d <= 88:
#        return 50000, 65536 * 3
#    if d <= 94:
#        return 60000, 65536 * 9
#    return 100000, 65536 * 9

def siqs_choose_nf_m(d):
    """Choose parameters nf (sieve of factor base) and m (for sieving
    in [-m,m].
    """
    # Using similar parameters as msieve-1.52
    if d <= 34:
        return 200, 272
    if d <= 36:
        return 300, 546
    if d <= 38:
        return 400, 1094
    if d <= 40:
        return 500, 2188
    if d <= 42:
        return 600, 4376
    if d <= 44:
        return 700, 8750
    if d <= 48:
        return 1000, 17500
    if d <= 52:
        return 1200, 35000
    if d <= 56:
        return 2000, 45000
    if d <= 60:
        return 4000, 60000 # 65536 * 3
    if d <= 66:
        return 6000, 60000 # 65536 * 3
    if d <= 74:
        return 10000, 120000 # 65536 * 3
    if d <= 80:
        return 30000, 120000 # 65536 * 3
    if d <= 88:
        return 50000, 240000 #65536 * 3
    if d <= 94:
        return 60000, 240000
    return 100000, 480000 # 65536 *6


def siqs_factor_base_primes(n, nf):
    """Compute and return nf factor base primes suitable for a Quadratic
    Sieve on the number n.
    """
    global small_primes
    factor_base = []
    for p in small_primes:
        if is_quadratic_residue(n, p):
            t = sqrt_mod_prime(n % p, p)
            lp = round(math.log2(p))
            factor_base.append(FactorBasePrime(p, t, lp))
            if len(factor_base) >= nf:
                break
    return factor_base


def sqrt_mod_prime(a, p):
    """Return the square root of a modulo the prime p. Behaviour is
    undefined if a is not a quadratic residue mod p."""
    # Algorithm from http://www.mersennewiki.org/index.php/Modular_Square_Root
    assert a < p
    #assert is_probable_prime(p)
    if a == 0:
        return 0
    if p == 2:
        return a
    if p % 2 == 0:
        return None
    p_mod_8 = p % 8
    if p_mod_8 == 1:
        # Shanks method
        q = p // 8
        e = 3
        while q % 2 == 0:
            q //= 2
            e += 1
        while True:
            x = random.randint(2, p - 1)
            z = pow(x, q, p)
            if pow(z, 2 ** (e - 1), p) != 1:
                break
        y = z
        r = e
        x = pow(a, (q - 1) // 2, p)
        v = (a * x) % p
        w = (v * x) % p
        while True:
            if w == 1:
                return v
            k = 1
            while pow(w, 2 ** k, p) != 1:
                k += 1
            d = pow(y, 2 ** (r - k - 1), p)
            y = (d ** 2) % p
            r = k
            v = (d * v) % p
            w = (w * y) % p
    elif p_mod_8 == 5:
        v = pow(2 * a, (p - 5) // 8, p)
        i = (2 * a * v * v) % p
        return (a * v * (i - 1)) % p
    else:
        return pow(a, (p + 1) // 4, p)

def siqs_find_factors(n, perfect_squares, smooth_relations):
    """Perform the last step of the Self-Initialising Quadratic Field.
    Given the solutions returned by siqs_solve_matrix_opt, attempt to
    identify a number of (not necessarily prime) factors of n, and
    return them.
    """
    factors = []
    rem = n
    non_prime_factors = set()
    prime_factors = set()
    for square_indices in perfect_squares:
        fact = siqs_factor_from_square(n, square_indices, smooth_relations)
        if fact != 1 and fact != rem:
            if larsprimetest(fact):
                if fact not in prime_factors:
                    print ("SIQS: Prime factor found: %d" % fact)
                    prime_factors.add(fact)

                while rem % fact == 0:
                    factors.append(fact)
                    rem //= fact

                if rem == 1:
                    break
                if larsprimetest(rem):
                    factors.append(rem)
                    rem = 1
                    break
            else:
                if fact not in non_prime_factors:
                    print ("SIQS: Non-prime factor found: %d" % fact)
                    non_prime_factors.add(fact)

    if rem != 1 and non_prime_factors:
        non_prime_factors.add(rem)
        for fact in sorted(siqs_find_more_factors_gcd(non_prime_factors)):
            while fact != 1 and rem % fact == 0:
                print ("SIQS: Prime factor found: %d" % fact)
                factors.append(fact)
                rem //= fact
            if rem == 1 or larsprimetest(rem):
                break

    if rem != 1:
        factors.append(rem)
    return factors

def is_quadratic_residue(a, p):
    """Return whether a is a quadratic residue modulo a prime p."""
    return legendre(a, (p - 1) // 2, 1, p) == 1

def legendre(a, q, l, n):
    x = q ** l
    if x == 0:
        return 1

    z = 1
    a %= n

    while x != 0:
        if x % 2 == 0:
            a = (a ** 2) % n
            x //= 2
        else:
            x -= 1
            z = (z * a) % n
    return z


def siqs_find_first_poly(n, m, factor_base):
    """Compute the first of a set of polynomials for the Self-
    Initialising Quadratic Sieve.
    """
    p_min_i = None
    p_max_i = None
    for i, fb in enumerate(factor_base):
        if p_min_i is None and fb.p >= SIQS_MIN_PRIME_POLYNOMIAL:
            p_min_i = i
        if p_max_i is None and fb.p > SIQS_MAX_PRIME_POLYNOMIAL:
            p_max_i = i - 1
            break

    # The following may happen if the factor base is small, make sure
    # that we have enough primes.
    if p_max_i is None:
        p_max_i = len(factor_base) - 1
    if p_min_i is None or p_max_i - p_min_i < 20:
        p_min_i = min(p_min_i, 5)

    target = math.sqrt(2 * float(n)) / m
    target1 = target / ((factor_base[p_min_i].p +
                         factor_base[p_max_i].p) / 2) ** 0.5

    # find q such that the product of factor_base[q_i] is approximately
    # sqrt(2 * n) / m; try a few different sets to find a good one
    best_q, best_a, best_ratio = None, None, None
    for _ in range(30):
        a = 1
        q = []

        while a < target1:
            p_i = 0
            while p_i == 0 or p_i in q:
                p_i = random.randint(p_min_i, p_max_i)
            p = factor_base[p_i].p
            a *= p
            q.append(p_i)

        ratio = a / target

        # ratio too small seems to be not good
        if (best_ratio is None or (ratio >= 0.9 and ratio < best_ratio) or
                    best_ratio < 0.9 and ratio > best_ratio):
            best_q = q
            best_a = a
            best_ratio = ratio
    a = best_a
    q = best_q

    s = len(q)
    B = []
    for l in range(s):
        fb_l = factor_base[q[l]]
        q_l = fb_l.p
        assert a % q_l == 0
        gamma = (fb_l.tmem * inv_mod(a // q_l, q_l)) % q_l
        if gamma > q_l // 2:
            gamma = q_l - gamma
        B.append(a // q_l * gamma)

    b = sum(B) % a
    b_orig = b
    if (2 * b > a):
        b = a - b

    assert 0 < b
    assert 2 * b <= a
    assert ((b * b - n) % a == 0)

    g = Polynomial([b * b - n, 2 * a * b, a * a], a, b_orig)
    h = Polynomial([b, a])
    for fb in factor_base:
        if a % fb.p != 0:
            fb.ainv = inv_mod(a, fb.p)
            fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
            fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

    return g, h, B


def siqs_find_next_poly(n, factor_base, i, g, B):
    """Compute the (i+1)-th polynomials for the Self-Initialising
    Quadratic Sieve, given that g is the i-th polynomial.
    """
    v = lowest_set_bit(i) + 1
    z = -1 if math.ceil(i / (2 ** v)) % 2 == 1 else 1
    b = (g.b + 2 * z * B[v - 1]) % g.a
    a = g.a
    b_orig = b
    if (2 * b > a):
        b = a - b
    assert ((b * b - n) % a == 0)

    g = Polynomial([b * b - n, 2 * a * b, a * a], a, b_orig)
    h = Polynomial([b, a])
    for fb in factor_base:
        if a % fb.p != 0:
            fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
            fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

    return g, h


def siqs_sieve(factor_base, m):
    """Perform the sieving step of the SIQS. Return the sieve array."""
    sieve_array = [0] * (2 * m + 1)
    for fb in factor_base:
        if fb.soln1 is None:
            continue
        p = fb.p
        i_start_1 = -((m + fb.soln1) // p)
        a_start_1 = fb.soln1 + i_start_1 * p
        lp = fb.lp
        if p > 20:
            for a in range(a_start_1 + m, 2 * m + 1, p):
                sieve_array[a] += lp

            i_start_2 = -((m + fb.soln2) // p)
            a_start_2 = fb.soln2 + i_start_2 * p
            for a in range(a_start_2 + m, 2 * m + 1, p):
                sieve_array[a] += lp
    return sieve_array

def siqs_trial_divide(a, factor_base):
    """Determine whether the given number a can be fully factorised into
    primes from the factors base. If so, return the indices of the
    factors from the factor base. If not, return None.
    """
    divisors_idx = []
    for i, fb in enumerate(factor_base):
        if a % fb.p == 0:
            exp = 0
            while a % fb.p == 0:
                a //= fb.p
                exp += 1
            divisors_idx.append((i, exp))
        if a == 1:
            return divisors_idx
    return None


def siqs_trial_division(n, sieve_array, factor_base, smooth_relations, g, h, m,
                        req_relations):
    """Perform the trial division step of the Self-Initializing
    Quadratic Sieve.
    """
    sqrt_n = math.sqrt(float(n))
    limit = math.log2(m * sqrt_n) - SIQS_TRIAL_DIVISION_EPS
    for (i, sa) in enumerate(sieve_array):
        if sa >= limit:
            x = i - m
            gx = g.eval(x)
            divisors_idx = siqs_trial_divide(gx, factor_base)
            if divisors_idx is not None:
                u = h.eval(x)
                v = gx
                assert (u * u) % n == v % n
                smooth_relations.append((u, v, divisors_idx))
                if (len(smooth_relations) >= req_relations):
                    return True
    return False


def siqs_build_matrix(factor_base, smooth_relations):
    """Build the matrix for the linear algebra step of the Quadratic Sieve."""
    fb = len(factor_base)
    M = []
    for sr in smooth_relations:
        mi = [0] * fb
        for j, exp in sr[2]:
            mi[j] = exp % 2
        M.append(mi)
    return M

def siqs_build_matrix_opt(M):
    """Convert the given matrix M of 0s and 1s into a list of numbers m
    that correspond to the columns of the matrix.
    The j-th number encodes the j-th column of matrix M in binary:
    The i-th bit of m[i] is equal to M[i][j].
    """
    m = len(M[0])
    cols_binary = [""] * m
    for mi in M:
        for j, mij in enumerate(mi):
            cols_binary[j] += "1" if mij else "0"
    return [int(cols_bin[::-1], 2) for cols_bin in cols_binary], len(M), m


def add_column_opt(M_opt, tgt, src):
    """For a matrix produced by siqs_build_matrix_opt, add the column
    src to the column target (mod 2).
    """
    M_opt[tgt] ^= M_opt[src]


def find_pivot_column_opt(M_opt, j):
    """For a matrix produced by siqs_build_matrix_opt, return the row of
    the first non-zero entry in column j, or None if no such row exists.
    """
    if M_opt[j] == 0:
        return None
    return lowest_set_bit(M_opt[j])

def siqs_solve_matrix_opt(M_opt, n, m):
    """
    Perform the linear algebra step of the SIQS. Perform fast
    Gaussian elimination to determine pairs of perfect squares mod n.
    Use the optimisations described in [1].

    [1] Koç, Çetin K., and Sarath N. Arachchige. 'A Fast Algorithm for
        Gaussian Elimination over GF (2) and its Implementation on the
        GAPP.' Journal of Parallel and Distributed Computing 13.1
        (1991): 118-122.
    """
    row_is_marked = [False] * n
    pivots = [-1] * m
    for j in range(m):
        i = find_pivot_column_opt(M_opt, j)
        if i is not None:
            pivots[j] = i
            row_is_marked[i] = True
            for k in range(m):
                if k != j and (M_opt[k] >> i) & 1:  # test M[i][k] == 1
                    add_column_opt(M_opt, k, j)
    perf_squares = []
    for i in range(n):
        if not row_is_marked[i]:
            perfect_sq_indices = [i]
            for j in range(m):
                if (M_opt[j] >> i) & 1:  # test M[i][j] == 1
                    perfect_sq_indices.append(pivots[j])
            perf_squares.append(perfect_sq_indices)
    return perf_squares


def siqs_calc_sqrts(square_indices, smooth_relations):
    """Given on of the solutions returned by siqs_solve_matrix_opt and
    the corresponding smooth relations, calculate the pair [a, b], such
    that a^2 = b^2 (mod n).
    """
    res = [1, 1]
    for idx in square_indices:
        res[0] *= smooth_relations[idx][0]
        res[1] *= smooth_relations[idx][1]
    res[1] = sqrt_int(res[1])
    return res

def sqrt_int(n):
    """Return the square root of the given integer, rounded down to the
    nearest integer.
    """
    a = n
    s = 0
    o = 1 << (math.floor(math.log2(n)) & ~1)
    while o != 0:
        t = s + o
        if a >= t:
            a -= t
            s = (s >> 1) + o
        else:
            s >>= 1
        o >>= 2
    assert s * s == n
    return s


def kth_root_int(n, k):
    """Return the k-th root of the given integer n, rounded down to the
    nearest integer.
    """
    u = n
    s = n + 1
    while u < s:
        s = u
        t = (k - 1) * s + n // pow(s, k - 1)
        u = t // k
    return s


def siqs_factor_from_square(n, square_indices, smooth_relations):
    """Given one of the solutions returned by siqs_solve_matrix_opt,
    return the factor f determined by f = gcd(a - b, n), where
    a, b are calculated from the solution such that a*a = b*b (mod n).
    Return f, a factor of n (possibly a trivial one).
    """
    sqrt1, sqrt2 = siqs_calc_sqrts(square_indices, smooth_relations)
    assert (sqrt1 * sqrt1) % n == (sqrt2 * sqrt2) % n
    return math.gcd(abs(sqrt1 - sqrt2), n)


def siqs_find_more_factors_gcd(numbers):
    res = set()
    for n in numbers:
        res.add(n)
        for m in numbers:
            if n != m:
                fact = math.gcd(n, m)
                if fact != 1 and fact != n and fact != m:
                    if fact not in res:
                        print("SIQS: GCD found non-trivial factor: %d" % fact)
                        res.add(fact)
                    res.add(n // fact)
                    res.add(m // fact)
    return res


def lowest_set_bit(a):
    b = (a & -a)
    low_bit = -1
    while (b):
        b >>= 1
        low_bit += 1
    return low_bit

def inv_mod(a, m):
    """Return the modular inverse of a mod m."""
    return eea(a, m)[0] % m


def eea(a, b):
    """Solve the equation a*x + b*y = gcd(a,b).
    Return (x, y, +/-gcd(a,b)).
    """
    if a == 0:
        return (0, 1, b)
    x = eea(b % a, a)
    return (x[1] - b // a * x[0], x[0], x[2])

def divsqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


""" Currently this only runs under unix ( I tested under Ubuntu), not OSX yet. I opened ticket
    https://github.com/alpertron/calculators/issues/16  with Alperton, so hopefully this gets
    fixed soon. sfactorint will soon be in it's own repo and will be pip installable. for now
    to use you must do the following commands from the primalitity git clone:
      cd calculators
      make
    
    These extra steps are worth it, sfactor can  then factor with Alperton ECM now, and it still
    uses it's underlying engine to factor numbers that ECM cannot which are included in 
    awesomenumberswecanfactor.txt and secretmessage.py

    Please execuse the lack of a pip install and non OSX compilation. i'm working with Alperton's
    creators with an open issue and am working on making a pip install verssion of sfactorint. 
    I include this manual method so you can get the full features of Alpertons ECM for factorization
    using python and i think you'll find the manual steps worth it. Thanks again and keep waiting 
    soon this will all be done automatically by an installer.
"""


def sfactorint(hm, returnwithpsuedoprimeresults=False):
   print(f"Attempting to factorise: {hm}")
   b = num = hm
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
       factors = sget_factors_lars_factorise(b)
       if factors == 0:
          print ("Could not factor due to ecm not being compiled")
          return 0
       for xx in factors:
           num = num // xx
           if returnwithpsuedoprimeresults == False:
             vv.append(xx)
           elif returnwithpsuedoprimeresults == True:
             vv.append((xx, larsprimetest(xx)))
     else:
           num = num // b
           if returnwithpsuedoprimeresults == False:
              vv.append(b)
           elif returnwithpsuedoprimeresults == True:
              vv.append((b, larsprimetest(b)))
     #if returnwithpsuedoprimeresults == False:
     #   vv.append(b)
     #elif returnwithpsuedoprimeresults == True:
     #   vv.append((b, larsprimetest(b)))
   if num != 1:
     if lprime == True:
       if returnwithpsuedoprimeresults == False:
          vv.append(num)
       elif returnwithpsuedoprimeresults == True:
          vv.append((num, larsprimetest(num)))
     elif lprime == False:
       if returnwithpsuedoprimeresults == False:
          vv.append(b)
       elif returnwithpsuedoprimeresults == True:
          vv.append((b, larsprimetest(b)))
   #print(vv)
   return vv


def sget_factors_lars_factorise(hm, offset=-2):
   num = hm
   vv = []
   while larsprimetest(num // 1) != True:
     print(vv, num)
     a = sfind_prime_evens_factorise(num, offset)
     if a == 0:
        return 0
     if type(a[5]) == list:
        vv.extend(a[5])
        for xx in a[5]:
           num = num // xx
        break
     #print(a)
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
     print(vv)
     num = num // vv[-1]
   if larsprimetest(num):
     vv.append(num)
   print(vv)
   return vv


def sfind_prime_evens_factorise(hm, offset=-2):
  y = 3
  prevtemp = 3
  if larsprimetest(hm):
     print(f"{hm} is already prime")
     return hm
  while True:
    if y.bit_length() > hm.bit_length() -1:
      if len(str(hm)) < 17:
         print(f"Attempting  to factorise {hm} with trial division")
         prevtemp = trial_division(hm)
         if prevtemp != hm:
            print(f"Trial Division Success")
            break
         else:
           print(f"Attempting  to factorise {hm} with POLLARD_BRENT")
           while prevtemp != hm:
              prevtemp = pollard_brent_lars_opt(hm)
           print(f"POLLARD_BRENT Success")
      else:
         print(f"Attempting  to factorise {hm} with POLLARD_BRENT")
         prevtemp = pollard_brent_lars_opt(hm)
      if hm == prevtemp:
         print(f"Attempting to factorise {hm} with Alperton ECM")
         try:
           process = Popen(["calculators/ecm", str(hm)], stdout=PIPE)
         except:
           print()
           print()
           print("caclulators/ecm doesn't exist")
           print("You can fix this by:")
           print("cd calculators")
           print("make")
           print()
           print("This should create ecm and you'll be able to use sfactorint.")
           print("Currently this works under ubuntu and should work with other")
           print("distributions. It does not work with OSX, i have an open")
           print("ticket with Alperton about this.")
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
         prevtemp.append(int(factorsstring.replace(' ', '')))

         #prevtemp = siqs_factorise(hm)
         print("Alperton ECM Success")
      else:
            print("POLLARD BRENT Success")
      break
    j = powers(hm, y)
    temp = j
    if j != 1 and j != 0:
      temp = j
      temp = hm % temp
      if temp == 0:
         prevtemp = temp
         print("c: break")
         break
      while temp != 1 and temp != 0:
         prevtemp = temp
         temp = hm % temp
    if temp == 0:
      print("h: break")
      break
    y = Xploder(y) -offset
  return hm, j, y.bit_length(), y, temp, prevtemp


def checkifpowersof2(N):
  return (N & (N-1) == 0) and N != 0

def checkifmersenne(N):
  return (N+1 & (N) == 0) and N != 0

# skiptrace(N)

"""   This is Based on finding factors down to the mersenne type numbers that bring N to 0 in mersenne type iterations, The variable lands on a  value which from an offset
      that makes for a perfect fermat test which i've tested to over a billion numbers without error using this format. This leads me to beleive there is a mathematics
      and equation that makes for a perfect fermat test with one number and an offset of 5 from that number. I'm searching for it and hoping others are as well. This 
      program is a Siever that is slower than prime sieve, but shows that you can build billions of primes without seiving with some speed and in an algorithmic way
      to eliminate errors with a pow test that is algorithmic and the same format for every number. 
      The equation for s = a = ( int(str(N+N),16) + int(str(int(str(N),16)+int(str(N),16))) ) is the same equation that I use to create high low maps in numbers using
      a base 10 to 16 relationship in those numbers. For example, if you had the number 6715923586739214200421, the equation builds the perfect form high low map to the 
      number as so wihout using a for loop, using pure math:

        6715923586739214200421
      0x1101100111101000000000  
 
     That binary number was created with ( int(str(N+N),16) - int(str(int(str(N),16)+int(str(N),16))) )//6 . Pure math to create a high low map of a number. I reversed the
     operation to be an add, and whoah, it created an algorithmic number that reduces to 0 in cycles of 1,3,7,15,31,63,127,255,511,1023,2047,4095,8191, etc. At the point
     these operations hit those numbers N will then converge on 0. (s) will converge on a number that a pow test offset from 2 less to 2 above always passes the fermat test
     when you first remove factors from the numbers during the descent to 0. The xx section below is the section that finds those factors, which allows me to have the perfect
     algorithmic fermat test which i tested to over 10 billion numbers without error. There is no isprime test here ( except with withstats=True option, for verification and
     understanding of what the final numbers are on that passes an isprime test. )  You can use this as an alternative to Sieveing, but it's slower to due it's descent to 0
     to create a perfect algroithmic fermat test and finding of factors. It was an intellectual exercise and I wanted to see what i could create that was unique and different
     from any published method to create all primes to a certain length. And I used an equation that creates a hi/low map to make it happen. Other equations did not work, so 
     I was intrigued by the power of that equation and plan to study it more. It is also an original unique creation i found and wanted to show off what it can do

     So no randomness is required for a fermat test to find the primes, the algorithim creates the perfect (s) which always passed the fermat test with an offset of 2. It is 
     a seiving program without using seiving math. You could consider it an isprime or factorization engine, but it wasn't designed for large numbers, only to show that we
     can create algorithmic fermat tests and seiving with the right algorithms 
  
     Here are some examples:

     In [4448]: skiptrace(1009732533765211)                                                                                                                                                    
     Out[4448]: False

     In [4447]: skiptrace(1009732533765211, factor=True) 
     N==1355457106081, M==899444200464828, (s * N ) + a  = 868062151967875342022144215 , a = 4624119960799520836, origN == 1009732533765211, larsprimetest(origN) == False,
     s==640420226836659, count/iterations to 0 == 1078
     xx factor test (factor found): 11344301, primecandidate == False, count/iterations to find factor: 1078

     Also, pow_mod_p2 is 4x  to 5x faster with powers of 2 than pythons pow function, that's why i use it and more information can be found above in the code.
     to use from larsprime import skiptrace
"""

def skiptrace(N, limit=1, withstats=False, xxrange=5, factor=False): 
    if N in [2, 3, 5, 7, 179]:
       return True  
    if xxrange == 5 and factor==True:
       xxrange = 1000
       withstats = True
    primenum = 3 
    origN = N  
    exception = True
    primecandidate = False
    s = a = ( int(str(N+N),16) + int(str(int(str(N),16)+int(str(N),16))) ) 
    M = p = (s * (1<<(N).bit_length() ) - 1 ) % N 
    sbreak = False 
    count = 0 
    

    for s in range(2,2**100): 
     N = pow_mod_p2(origN, 4, (1<<(origN).bit_length()))  
     for x in range(0,limit): 
      count +=1  
      N =  abs(pow_mod_p2(s, 4, (1<<(origN).bit_length()) ))
      try:
         s = abs(( (s * N ) + a )) % (M)  
      except:
          s = abs(( (s * N ) + a  )) % ((s * (1<<(N).bit_length() ) ) )
          exception = True
      l =  math.gcd(s+N, origN) 
      prime = math.gcd(s, origN) 

      if N == 0 and factor == False:
         if checkifmersenne(count):
            primenum = count
         if pow(count, origN-1, origN) == 1 and pow(count+1, origN-1, origN) == 1 and pow(((s * N ) + a) +1, origN-1, origN) == 1:
            if withstats == True:
              print(f"N=={N}, M=={M}, (s * N ) + a  = {(s * N ) + a} , a = {a}, origN == {origN}, larsprimetest(origN) == {larsprimetest(origN)}, s=={s}, count/iterations to 0 == {count}") 
            if pow( (s * N ) + a , origN-1, origN) > 1 or pow( s - 1 , origN-1, origN) > 1 or pow( s - 2 , origN-1, origN) > 1:
              if withstats == True:
                print("N==0, Failed pow test, Not Prime")
              return False
            else:
              return True
         else:
            if withstats == True:
              print("N==0, Failed pow test, Not Prime")
            return False

      xx = [math.gcd(s, origN)] + [math.gcd(s*p+x,origN) for x in range(xxrange)] + [math.gcd(s*p-x,origN) for x in range(1,xxrange)]
      try:
         prime = min(list(filter(lambda x: x not in set([1]),xx)))
      except:
        prime = 1
      if prime == 1:
         continue
      else:
          if prime == origN and pow(2, origN-1, origN) == 1 and pow(count+1, origN-1, origN) == 1 and pow(primenum+1, origN-1, origN) == 1 and pow(N+1, origN-1, origN) ==1:
             primecandidate = True
          if withstats == True:
              print(f"N=={N}, M=={M}, (s * N ) + a  = {(s * N ) + a} , a = {a}, origN == {origN}, larsprimetest(origN) == {larsprimetest(origN)}, s=={s}, count/iterations to 0 == {count}") 
              print(f"xx factor test: {prime}, primecandidate == {primecandidate}, count/iterations to find factor: {count}")
          return primecandidate 


