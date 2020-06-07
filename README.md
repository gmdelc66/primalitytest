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

**  UPDATE JUNE 1st 2020 **

Added non probabalistic miller_rabin Primality Test: primality_test_miller_rabin_non_random(num)

**  UPDATE JUNE 3rd 2020 **

Added a PrimeMaker that is unique in that it uses an algorithm with random numbers to find a prime candidate.
It uses a feature of prime numbers to find a random number that fits with this feature to find a candidate. If the 
algorithm finds the right number, we run a fermat test and prime test on the number, and if that passes, the algorithm
has found a prime number. The usage of this contains a stats return and a normal number return. It's normal usage
is: larsprimemaker(lowend, highend). Example:


In [6847]: larsrandomprimemaker(2 ** 1500-1,2 ** 1501-1)                                                                           


Out[6847]: 31067962887757566410080873561344849881557449576202385732055546909175507216526707451692981056410284062278732943683623854676445585775624901181668416997590554810831965826094566372012144586447920086656435517508317490622197559416770742121378627557888057672986949466779433278653219360454629141938765082151613807779917411713563311726105689176647642309519555996729277937695498095900436523818222813858507326110770693966246894366187329435444062123638469833554861

**  UPDATE JUNE 4th 2020 **

For Educational purposes, i have added some probabalistic functions to create primes. I think you'll be suprised at it's
ability to create and pass isprime tests even though it's probabalistic. I include them because they are simple, yet
impressive at their ability to pass isprime tests, even if error prone. All numbers created with these must be greater than
2 ** 50. You can use mersenne numbers to generate primes that don't pass this test so don't use for anything serious, it is more for it's uncanny ability to make prime numbers when mersenne numbers aren't involved

fast_probabilistic_isprime(num)

fast_probabilistic_next_prime(num)

create_probabilistic_prime(num)

larsprobabilisticprimemaker(smallnum, largenum) with optional withstats=True

** UPDATE JUNE 5th 2020 **

Added powers_of_2_prime_maker()

Added random_powers_of_2_prime_finder(num, withstats=True)  Make sure to use this one with withstats=True, it returns
the equation used to create the prime number. If you want only primes to make your prime, you can also use with the form
random_powers_of_2_prime_finder(num, primeanswer=True, withstats=True)

    In [84]: random_powers_of_2_prime_finder(851,primeanswer=True,withstats=True)                                                                                                                      
    Out[84]:  'pow_mod_p2(7468640369567690346277031725921067016706177332289807891356998034529771885290124399269326996099882789561557590658564984484253714276765824475522164776339997224079871722801903655983815167082438045248760487514826078683500121225395239128728007404895402241638073, 2**851-1, 2**851) = 1218548584186184239623670215597350938823269250753905053144018814946076930755807832037241993034307736126474140774823031555801868349013725458150038095791115446136783675530875149076659748418028022464383293319718032939862155683442828981933195529768427075495817'
    
    In [3]: random_powers_of_2_prime_finder(851,primeanswer=True,withstats=True)                                                                                                                       
    Out[3]: 'pow_mod_p2(4511121199374001167238614392992811348861935845102009166129977507158398195740673990762566168149226982656693807749355310704794737211204262510232752305803725343148144960209125047922397384983494031809135452902219128315134883839002887979281590057356646519644739, 2**851-1, 2**851) = 8956169857539619894363696438807801656445892172576181602346502930948766646456948658634014483680814513843042992560547872707700277192599584808991867332510773119687154946351635397847478125401767110092102839656067696243247003088924707759407112829694455639718507'

    You can then take the two results and create a large psuedo prime 1218548584186184239623670215597350938823269250753905053144018814946076930755807832037241993034307736126474140774823031555801868349013725458150038095791115446136783675530875149076659748418028022464383293319718032939862155683442828981933195529768427075495817 * 8956169857539619894363696438807801656445892172576181602346502930948766646456948658634014483680814513843042992560547872707700277192599584808991867332510773119687154946351635397847478125401767110092102839656067696243247003088924707759407112829694455639718507 = 10913528099635883221041560804874685150499478408666670014248547043155182789618340406359280437122609145359145915049131461835554843530574025879821940625507684259239123134972160121784779848974383883037791635562021850383405965485731347741136467659016299148726209683332270112284900236176466741464515835693945079967086188371437878262846517955567474191635498829381970586399684013060901447628935810161949401956844301595836037647123747524173250580741189032427218189484295468889109455413328293788552703781965069295335985219
    
    I would suggest using the shorter form random_powers_of_2_prime_finder(851,withstats=True) and using those two results for
    creating your larger psuedoprime based on the results, as finding a result is much faster when not searching for a prime 
    answer as well. But maybe it's more secure to have only a prime answer, to create a prime result, so for those who may     
    think so, i included it as an option. Just be aware it's much slower, about 10x to 20x slower than building a straight
    prime without a psuedoprime x for pow(x, powersof2-1, powersof2)



""" powers_of_2_prime_maker() Here is it's description:
    Use any number here but use the sieves numbers here to see that only prime numbers can make prime numbers
    via pow(xx, 2 ** x-1, 2 ** x) where all the primes are also in the pow statement, meaning there is a 1 to
    1 ratio of a pow(prime) with it's answer. xx is a prime number and x is the iteration of the loop. For example:
    
    In [8128]: powers_of_2_prime_maker(6)                                                                                                                                     
    pow(53, 2 ** 6-1, 2 ** 6) = 29 and is Prime, 53 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    pow(43, 2 ** 6-1, 2 ** 6) = 3 and is Prime, 43 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    pow(31, 2 ** 6-1, 2 ** 6) = 31 and is Prime, 31 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    pow(29, 2 ** 6-1, 2 ** 6) = 53 and is Prime, 29 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    pow(13, 2 ** 6-1, 2 ** 6) = 5 and is Prime, 13 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    pow(5, 2 ** 6-1, 2 ** 6) = 13 and is Prime, 5 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    pow(3, 2 ** 6-1, 2 ** 6) = 43 and is Prime, 3 is Prime?: True, 2 ** 6-1 is Prime?: False
    
    In [8129]: powers_of_2_prime_maker(7)                                                                                                                                      
    7: 127 already Prime
    
    pow(113, 2 ** 7-1, 2 ** 7) = 17 and is Prime, 113 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(109, 2 ** 7-1, 2 ** 7) = 101 and is Prime, 109 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(107, 2 ** 7-1, 2 ** 7) = 67 and is Prime, 107 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(101, 2 ** 7-1, 2 ** 7) = 109 and is Prime, 101 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(79, 2 ** 7-1, 2 ** 7) = 47 and is Prime, 79 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(67, 2 ** 7-1, 2 ** 7) = 107 and is Prime, 67 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(53, 2 ** 7-1, 2 ** 7) = 29 and is Prime, 53 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(47, 2 ** 7-1, 2 ** 7) = 79 and is Prime, 47 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(43, 2 ** 7-1, 2 ** 7) = 3 and is Prime, 43 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(29, 2 ** 7-1, 2 ** 7) = 53 and is Prime, 29 is Prime?: True, 2 ** 7-1 is Prime?: True
   
    pow(17, 2 ** 7-1, 2 ** 7) = 113 and is Prime, 17 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    pow(3, 2 ** 7-1, 2 ** 7) = 43 and is Prime, 3 is Prime?: True, 2 ** 7-1 is Prime?: True
    
    Use https://www.mersenne.org/primes/  to find which primes are mersenne primes to test. Notice that in both
    cases the numbers generated show up as the first number in the pow() statement that generate a true prime,
    and there is never a  false in the case of 2 ** -1 numbers. I thought this was interesting so included it in this 
    library.
    
    Notice that it seems that all numbers that end up as an answer are also seem to end up in the first pow(x,,)
    statement
   
    random_powers_of_2_prime_finder(powersnumber, withstats=False)
   
    Here is a random powers of 2 prime finder. Instead of a traditional random number find and next_prime find, 
    It finds a random number that passes the lars_last_modulus_powers_of_two and checks if it's answer which is 
    (randomnum//2): pow(answer, 2 ** powersnumber-1, 2 ** powersnumber) passes an is prime test and continues until it
    finds a prime number as the answer.
    
    Here is an example if withstats is True:
    In [8376]: random_powers_of_2_prime_finder(500,withstats=True)                                                                                                         
    Out[8376]: 'pow(666262300770453383069409586449388105866418680981109533955324455061042093893855903254102021029841224158334524986498089277831523295501050122115012763111, 2 ** 500-1, 2 ** 500) = 896210381184287864297818969694142462892609158257898833237071849213575043971828530532195572986889116466526908364900915586299134290481831272303561385431'
    
    It returns an equation showing the prime result, here is another example:
    
    In [8436]: random_powers_of_2_prime_finder(100,withstats=True)                                                                                                         
    Out[8436]: 'pow(21228499098241391741518188355, 2**100-1, 2**100) = 648150045025216535003765994859'
 
    Notice the answer is an equation that finds a prime.
"""

UPDATE JUNE 6th 2020

refactored a new larsisprime(num) to be a more concise version of larsprimetest. It is currently in beta. It utilizes
lars_last_modulus_powers_of_two as any number that has a lars_last_modulus_powers_of_two(num+num) != 2 will never be prime, it's a quick way to discard non primes.

Added larsgcd which larsisprime() utilizes:

    larsgcd(num) returns any primes found within the offset of it's powers of two number.
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

** UPDATE JUNE 7th 2020 **

added: get_factors_lars_opt(num)  which uses an optimized pollard brent to find larger factors

    get_factors_lars_opt is a combination of the routines above and a pollard brent optimization i made to
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

-------------

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


 get_factors(2 ** 200-1)
 
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
    
    112%64
    
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
