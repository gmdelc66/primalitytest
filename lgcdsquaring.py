""" The following was an experiment in finding primes by squaring, rather than square rooting. 
    One issue I came up with while square rooting, is a precision issue with math.sqrt not 
    correctly working over numbers of a certain size. I decided to try to see if I could find
    primes by squaring a number instead and after this is what i came up with. It is not based
    on any other theorems, it's an original creation, and while slow for larger factors, it works
    well for an experiment into finding prime numbers. Based on this, i beleive all prime factors
    can be found with this method, but modulus arithmitic down the entire path of a square number
    it has no practicle value other than to show that all primes can be found using this method.

    Here are some example results using squaring rather than square rooting for finding primes:

    In [1414]: lgcdsquaring(10097325337652031009732533765203, searchlimit=150)                                                                                                        
    Out[1414]: [353, 1823, 1409, 449, 641, 3163, 69857, 175113847]

    In [1415]: lgcdsquaring(10097325337652011009732533765201)                                                                                                                         
    Out[1415]: [17, 9, 3, 41, 353, 449, 1409, 641, 2417, 69857, 22198987]

    In [1442]: lgcdsquaring(314159314159314159314159, searchlimit=150)                                                                                                                
    Out[1442]: [101, 73, 137, 9901, 314159, 99990001]    

    I created this as an experiment and it worked and works well. I include it here to show ways
    of finding primes that are not traditional and may be of interest into those learning about prime
    numbers and different methods of factoring not based on published material, but rather learning of 
    ways to find prime numbers on your own. Those learning about prime solving may find this an 
    interesting approach and may want to pursue writing their own version of this until getting to more
    advanced material. If a fast modular reduction shortcut could be found, this would be a very fast
    algorithm.

    To use:
   
    from lgcdsquaring import *

""" 

import random
import math

def fermatsprimetest(hm, iterx=150):
   for x in range(iterx):
     if pow(random.randint(2,hm-1), hm-1, hm) != 1:
        return False
   return True

def lgcdsquaring(hm, searchlimit=25):
   vv = []
   prevhm = 0
   while hm != 1:
     if fermatsprimetest(hm) == True:
        vv.append(hm)
        break
     else:
        if prevhm != hm:
          res = search_for_prime(hm, searchlimit)
          vv.append(res)
        else:
           print (f"No further factors found with squaring searchlimit={searchlimit}")
           vv.pop()
           vv.append(hm)
           break
     prevhm = hm
     hm = hm // vv[-1]
   return vv

def search_for_prime(hm, searchlimit=25):
   for x in range(1,searchlimit):
       answer = gcd_mod_find(pow(hm,x), hm)
       if answer != 1:
           break
   return answer #, pow(hm,x)

def gcd_mod_find(hm, find):
    prevcr = hm
    getcr =  hm%(1<<(hm).bit_length()-1)
    bitlength = hm.bit_length()
    count=0
    found = False
    while getcr != 0 and getcr != 1 and bitlength > count:
       count+=1
       temp = hm%getcr
       prevcr = getcr
       getcr = temp
       answer = math.gcd(prevcr, find)
       if answer != 1:
          if (answer != 0) and (answer & (answer-1) == 0):
             answer = 2
          found = True
          break
    if found == True:
       return answer
    else:
       if (hm != 0) and (hm & (hm-1) == 0):
          return 2
       else:
          return 1 
