# primalitytest
Test the primality of numbers ( non probabilistic test)  

This is a non probabilistic primality test. It peforms fermat's test from the bitlength of the number down to 2. 
It then uses my algorithim to determine whether a number is composed of small primes. 
If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
works via algorithims which do not use randomness to reduce errors and shows that all primes can be found be squaring
a number until all factors are found

** UPDATE MAY 31st 2020 **

Added fast modulus reduction technique for modulus powers of 2: get_last_modulus_powers_of_two()
Added fast modulus reduction technique to rebuild an entire number: powers_nonfactorization_quantum_leap()
Added fuzzy_factor_p2()
Added fuzzy_factor_time_constrained()


To use:

from larsprime import *

larsprimetest(1009)
##  True

lars_next_prime(1013)
##  1019


The following is a composite reduction method. Instead of reducing a number to primes, it reduced them to composite
numbers only. It is included for those interested in seeing non prime factorization reduction of numbers:

try_nonfactorization_mod(1009)

[1, 16, 2, 2, 2, 2, 2]

build_composite_number([1, 16, 2, 2, 2, 2, 2]) 

1009

--------------


You can use this module for factorization as well, but until a super fast modular reduction algorithm is found it is 
not practical for use as there are faster factorization algorithms available, but i include it to show my theory is 
sound for primality testing.

get_factors(100973253376634432)

Out[1496]: [2, 2, 2, 2, 2, 2, 5419, 54403, 5351609]


get_factors(29**10)

Out[1500]: [29, 29, 29, 29, 29, 29, 29, 29, 29, 29]

get_factors(10099*24389)

Out[1502]: [29, 29, 29, 10099]


 get_factors(2**200-1)
 
 [3, 5, 11, 41, 5, 5, 17, 31, 101, 401, 251, 601, 1801, 8101, 4051, 61681, 2787601, 268501, 340801, 3173389601]
 
 
 --------------------
 
 Fuzzy Factor introduced. Example usage: fuzzy_factorp2(2 ** 1000-1) or fuzzy_factorp2(2 ** 1000-1, True)
 
 From it's comments in the code section:
 
   Fuzzy factor was designed for finding psuedoprimes near powers of 2 numbers that can be reduced faster than a 
   straight factorization using many differerent algotihims. For example, Try: fuzzy_factorp2(2 ** 1200-1, True) and 
   you get an almost instantaneous result with only 3 numbers that are False (psuedoprime). You can plug these numbers
   into PARI or ECM and they can factor the numbers faster than you can by using PARI and ECM to reduce just the
   2 ** 1200-1 itself.  PARI can't seem to factor 2 ** 1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2 ** 1200-1.
 
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number.

   What is *AMAZING* about fuzzy_factor. https://www.alpertron.com.ar/ECM.HTM cannot reduce 2 ** 1000-1, but using 
   fuzzy_factor, you can take the psuedoprime components, plug them into ECM, and fully reduce 2 ** 1000-1 in a few
   minutes, as fuzzy_factor reduces the number into psuedoprimes that can be reduced further by ECM instead of a
   straight factorization of 2 ** 1000-1. Use fuzzy_factorp2(2 ** 1000-1, True) to get results back with whether the
   number is prime (True) or psuedoprime (False). You can then plug the False numbers into ECM to reduce the number
   into all of its factors. The default is False so you can use with build_prime_number() to build the original number 
   from the fuzzy factors. You can also try this with 2 ** 500-1 and other numbers to see it's usefulness in combination
   with other factorization engines.

--------------

    Fastest modulus reduction of powers of two which i discovered while studying primes. Other shortcuts may 
    exist i'm looking for them too to speed up my modulus reductions above. This is the same as doing the
    
    following:
    
    1008%512
    
    # 496
    
    496%256
    
    # 240
    
    240%128
    
    # 112
    
    112^64
    
    # 48
    
    48%32
    
    # 16
    
    16%16 
    
    # 0
    
    With get_last_modulus_powers_of_two(1008) you will get the answer 16 immediately. This works for all numbers
    walking down a modulus powwers of two tree without having to walk down the tree. I would urge mathemeticians
    to look for other shortcuts like this so I can speed up my other modulus reductions. I'm searching for them as
    well
    
    In [2601]: get_last_modulus_powers_of_two(1008)                                                                                                
    Out[2601]: 16
    
    
---------------

""" Fuzzy factor was designed for finding psuedoprimes near powers of 2 numbers that can be reduced faster than a 
   straight factorization using many differerent algotihims. For example, Try: fuzzy_factor(2 ** 1200-1, True) and 
   you get an almost instantaneous result with only 3 numbers that are False (psuedoprime). You can plug these numbers
   into PARI or ECM and they can factor the numbers faster than you can by using PARI and ECM to reduce just the
   2 ** 1200-1 itself.  PARI can't seem to factor 2 ** 1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2 ** 1200-1.
    
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number.
   What is *AMAZING* about fuzzy_factor. https://www.alpertron.com.ar/ECM.HTM cannot reduce 2 ** 1000-1, but using 
   fuzzy_factor, you can take the psuedoprime components, plug them into ECM, and fully reduce 2 ** 1000-1 in a few
   minutes, as fuzzy_factor reduces the number into psuedoprimes that can be reduced further by ECM instead of a
   straight factorization of 2 ** 1000-1. Use fuzzy_factor(2 ** 1000-1, True) to get results back with whether the
   number is prime (True) or psuedoprime (False). You can then plug the False numbers into ECM to reduce the number
   into all of its factors. The default is False so you can use with build_prime_number() to build the original number 
   from the fuzzy factors. You can also try this with 2 ** 500-1 and other numbers to see it's usefulness in combination
   with other factorization engines.

   Here is an example output, try this with your favorite factorization engine in comparison to this usage:

   In [5]: build_prime_number(fuzzy_factorp2(2 ** 1200-1))                                                                                                                  
   Out[5]:
17218479456385750618067377696052635483579924745448689921733236816400740691241745619397484537236046173286370919031961587788584927290816661024991609882728717344659503471655990880884679896520055123906467064419056526231345685268240569209892573766037966584735183775739433978714578587782701380797240772477647874555986712746271362892227516205318914435913511141036261375

   fuzzy_factorp2(2 ** 1200-1,True) 

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
  current straight PARI or ECM factorizations of 2 ** 1200-1.
