# primalitytest
Test the primality of numbers ( non probabilistic test)  

This is a non probabilistic primality test. It preforms fermat's test from the bitlength of the number down to 2. 
It then uses my algorithim to determine whether a number is composed of small primes. 
If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
works via algorithims which do not use randomness to reduce errors


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
