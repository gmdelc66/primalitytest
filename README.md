# primalitytest
Test the primality of numbers ( non probabilistic test)

This is a non probabilistic primality test. It preforms fermat's test from the bitlength of the number down to 2. 
It then uses my algorithim to determine whether a number is composed of small primes. 
If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
works via algorithims which do not use randomness to reduce errors


To use:

from primetest import *

larsprimetest(1009)
##  True

lars_next_prime(1013)
##  1019
