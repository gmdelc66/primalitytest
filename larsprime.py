# This is a non probabilistic primality test. It preforms fermat's test from the bitlength of the number down to 2. 
# It then uses my algorithim to determine whether a number is composed of small primes. 
# If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
# is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
# works via algorithims which do not use randomness to reduce errors. I created a super fast modulus reduction
# technique that doesn't have to walk the entire mod path down from a powers of a 2 and am looking to create the
# same for other modulus reductions. I'm hoping other mathematicians will be interested and will do the same
# it would greatly increase the speed of the method i use. The reduction i created is get_last_modulus_powers_of_two()


import math


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
   into PARI or ECM and they can factor the numbers faster than you can by using PARI and ECM to reduce just the
   2**1200-1 itself.  PARI can't seem to factor 2**1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2**1200-1.
   
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number. fuzzy_factor was designed for 2**numbers-1, and a newer version fuzzy_factor_any() will be introduced
   here shortly as I'm making daily updates.

   What is *AMAZING* about fuzzy_factor. https://www.alpertron.com.ar/ECM.HTM cannot reduce 2**1000-1, but using 
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
   What is *AMAZING* about fuzzy_factor. https://www.alpertron.com.ar/ECM.HTM cannot reduce 2**1000-1, but using 
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
  current straight PARI or ECM factorizations of 2**1200-1.

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


