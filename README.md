# primalitytest
Test the primality of numbers ( non probabilistic test)  

This is a non probabilistic primality test. It peforms fermat's test from the bitlength of the number down to 2. 
It then uses my algorithim to determine whether a number is composed of small primes. 
If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
works via algorithims which do not use randomness to reduce errors and shows that all primes can be found be squaring
a number until all factors are found


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
 
 Fuzzy Factor introduced. Example usage: fuzzy_factor(2 ** 1000-1) or fuzzy_factor(2 ** 1000-1, True)
 
 From it's comments in the code section:
 
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

