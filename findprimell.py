""" To use this library, use:
    from findprimell import *
"""

""" While answering:
    https://stackoverflow.com/questions/62365336/how-do-researchers-manage-to-find-such-large-primes
    I came across a math change to the Lucas Lehmer Algorithm that allowed it to find primes.
    This is the result of that work an I think you'll find it interesting. Here are some examples of 
    it in action:

    In [3]: sfactorPFLLint(1009732533765211)                                                                                                                                                  
    Attempting to factorise 1009732533765211 with PrimeFinderLucasLehmer
    Out[3]: [11344301, 89007911]

    In [4]:  sfactorPFLLint(8114231289041741)                                                                                                                                                 
    Attempting to factorise 8114231289041741 with PrimeFinderLucasLehmer
    Out[4]: [1839221, 4411776121]

    In [5]:  sfactorPFLLint(10142789312725007)                                                                                                                                                
    Attempting to factorise 10142789312725007 with PrimeFinderLucasLehmer
    Out[5]: [100711423, 100711409]

    In [8]:  sfactorPFLLint(2727272727272727272727272727)                                                                                                                                     
    Attempting to factorise 2727272727272727272727272727 with PrimeFinderLucasLehmer
    Attempting to factorise 909090909090909090909090909 with PrimeFinderLucasLehmer
    Attempting to factorise 303030303030303030303030303 with PrimeFinderLucasLehmer
    Attempting to factorise 101010101010101010101010101 with PrimeFinderLucasLehmer
    Attempting to factorise 1000100010001000100010001 with PrimeFinderLucasLehmer
    Attempting to factorise 34486207241413796552069 with PrimeFinderLucasLehmer
    Attempting to factorise 144293754148174880971 with PrimeFinderLucasLehmer
    Attempting to factorise 513500904441903491 with PrimeFinderLucasLehmer 
    Attempting to factorise 110454055590859 with PrimeFinderLucasLehmer
    Out[8]: [3, 3, 3, 101, 29, 239, 281, 4649, 909091, 121499449]

"""
    
from larsprime import *

def sfactorPFLLint(hm):
  vv = []
  while True:
   prime = sfactorintPFLL(hm)
   if prime != False:
      hm = hm//prime
      vv.append(prime)
   else: 
     print("Pseudoprime last answer")
     vv.append(hm)
     break
   if larsprimetest(hm):
     vv.append(hm)
     break
  return vv

def sfactorintPFLL(hm):
    print (f"Attempting to factorise {hm} with PrimeFinderLucasLehmer")
    find = PrimeFinderLucasLehmer4(hm)
    while larsprimetest(find) != True:
       if find == 1:
          break
       find = PrimeFinderLucasLehmer4(find)
    if find == 1: 
      print(f"PrimeFinderLucasLehmer did not succeed")
      return False
    else:
      return find

def PrimeFinderLucasLehmer4(N):
   p = 1<<N.bit_length()-1
   if p == 2:
     return True
   s = 4
   M = pow(p, 2) - 1
   for x in range (1, 1000000):
     s = (((s * N ) - 2 )) % M
     xx = [math.gcd(s, N),
           math.gcd(s*p+2, N),
           math.gcd(s*p+1, N),
           math.gcd(s*p, N),
           math.gcd(s*p-1, N),
           math.gcd(s*p-2, N)]
     try:
        prime = min(list(filter(lambda x: x not in set([1]),xx)))
     except:
        prime = 1
     if prime == 1:
        continue
     else:
        break
   #print (x, prime)
   return prime
