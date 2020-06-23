# primalitytest
Test the primality of numbers ( non probabilistic test)  and now factor with BRENT_POLLARD AND SKOLLMAN's SIQS
Implementation. ( And a new repo coming soon using Alperton's ECM )

To use this library simply do: from larsprime import *

** UPDATE JUNE 22nd 2020 **

I have now included sfactorint(num) which utilizes Alperton's ECM. Some caveates. This works under ubuntu and should
with other distributions, but not under OSX due to a macro compiler issue that im looking into. 

To use you must do the following manual commands( my apologies on this, i expect to make sfactorint into a new repo
that does this all automatically, but you will find it worth your while if you take the time to do it under linux.

from the primality directory clone, you must:

cd calculators

make

cd ..

then run ipython3  and 

from larsprime import *

or

from larsprime import sfactorint

All other libraries will still work without doing this, but sfactorint will not unless you perform these steps. For 
those who take the time under linux to do this you will get access to Alperton's Amazing factorization engine using
python. Here are some example factorizations with it. Alperton is amazing and now you can use this engine via ipython3
under linux.

    In [4]: sfactorint(2**320-27)                                                                                                                                                  
    Attempting to factorise: 2135987035920910082395021706169552114602704522356652769947041607822219725780640550022962086936549
    [] 19984846359923304131572718704765894820156942676449198185279536798495814090816533354649
    Attempting  to factorise 19984846359923304131572718704765894820156942676449198185279536798495814090816533354649 with POLLARD_BRENT
    Attempting to factorise 19984846359923304131572718704765894820156942676449198185279536798495814090816533354649 with Alperton ECM
    Alperton ECM Success
    [6541567246167498436733698138291429826932034878522265977444975810201, 3055054791591694849]
    Out[4]: 
    [433,
    2591,
    95267,
    6541567246167498436733698138291429826932034878522265977444975810201,
    3055054791591694849]

    In [5]: sfactorint(632459103267572196107100983820469021721602147490918660274601)                                                                                               
    Attempting to factorise: 632459103267572196107100983820469021721602147490918660274601
    [] 632459103267572196107100983820469021721602147490918660274601
    Attempting  to factorise 632459103267572196107100983820469021721602147490918660274601 with POLLARD_BRENT
    Attempting to factorise 632459103267572196107100983820469021721602147490918660274601 with Alperton ECM
    Alperton ECM Success
    [972033825117160941379425504503, 650655447295098801102272374367]
    Out[5]: [972033825117160941379425504503, 650655447295098801102272374367]
    
To show more of the power of Alpertons Engine here are two number we factor in less than 2 minutes: 

    In [57]: sfactorint(random_powers_of_2_prime_finder(125, withstats=False)*random_powers_of_2_prime_finder(125, withstats=False))                                               
    Attempting to factorise: 1071550297260944289721264733201372325018796026439823716133100011628159597217  
    [] 1071550297260944289721264733201372325018796026439823716133100011628159597217
    Attempting  to factorise 1071550297260944289721264733201372325018796026439823716133100011628159597217 with POLLARD_BRENT
    Attempting to factorise 1071550297260944289721264733201372325018796026439823716133100011628159597217 with Alperton ECM
    Alperton ECM Success
    [33010216959086694408014119851159034909, 32461170994090650736291845825264822613]
    Out[57]: 
    [33010216959086694408014119851159034909,
    32461170994090650736291845825264822613]
    # About 2 minutes to factor (76 digit number)

    In [58]: sfactorint(random_powers_of_2_prime_finder(75, withstats=False)*random_powers_of_2_prime_finder(150, withstats=False))                                                
    Attempting to factorise: 8804193098709564232326493425921587427217376241095831209316118109547
    [] 8804193098709564232326493425921587427217376241095831209316118109547
    Attempting  to factorise 8804193098709564232326493425921587427217376241095831209316118109547 with POLLARD_BRENT
    Attempting to factorise 8804193098709564232326493425921587427217376241095831209316118109547 with Alperton ECM
    Alperton ECM Success
    [935014548440225175815525480974308169870487261, 9416102790482313143527]
    Out[58]: [935014548440225175815525480974308169870487261, 9416102790482313143527]
    # Less than a minute factorization
    
    In [61]: sfactorint(random_powers_of_2_prime_finder(95, withstats=False)*random_powers_of_2_prime_finder(135, withstats=False))                                                
    Attempting to factorise: 466560005794735402042454434351319659915584814915000650616735677512903
    [] 466560005794735402042454434351319659915584814915000650616735677512903
    Attempting  to factorise 466560005794735402042454434351319659915584814915000650616735677512903 with POLLARD_BRENT
    Attempting to factorise 466560005794735402042454434351319659915584814915000650616735677512903 with Alperton ECM
    Alperton ECM Success
    114979000759810378698490339575093930957167, 31147605456202784218829895209]
    Out[61]: [14979000759810378698490339575093930957167, 31147605456202784218829895209]
    # Less than 2 minutes factorization

To use random_powers_of_2_prime_finder use: from larsprime import random_powers_of_2_prime_finder. It creates an equtaion to make the prime number which can be seen via withstats=True, instead of finding a random prime and looking for the next prime.

** END JUNE 22nd 2020 UPDATE **

You will most likely be using fuzzy_factorp2_factorise(num) but there are many different modules included.

This library has evolved from a primality test to a factorization engine, so i hope you enjoy the results. It can
factor very quickly and uses a few different methods for factoring and is a great alternative to sympy's factorint

Give fuzzy_factorp2_factorise(random.randrange(2 ** 180-1, 2 ** 181-1,2))  or
     fuzzy_factorp2_factorise(2402956925397989535742923204519510889236432671327589210309935) or 
     fuzzy_factorp2_factorise(2 ** 1200-1) or 
              fuzzy_factorp2_factorise(272727272727272727272727272727272727272727272727272727272727272727272727272727272727272727272727272727)  a try to see what 
     it's capable of.

From the primalitytest directory, you can utilize the entire library just by:  from larsprime import *

I included a secretmessage.py that includes a number that only fuzzy_factorp2_factorise(num) can factor, with a secret message 
about it's security. Try factoring the (N) in you favorite engine and see that only fuzzy_factor can factor it in less than 2 minutes. To run from the command line:  python3 secretmessage.py

Give it two minutes to factor and see from the secret message you could actually factor the number in nano seconds if you knew the hexified secret of the number. No engine i know of can factor(N). I desigined this number so we can factor it and include a message about its insecurity, even though it's hard to factor, it's easy to factor once you know it's secret

Until the new repo comes out, try fuzzy_factorp2_factorise(num) and sfactorPFLLint(num).  The former can be used by:
from larsprime import *
and the later:
from findprimell import *

They both utilize BRENT POLLARD AND FACTORISE.py. but underneath they both utilize different engines to factor smaller 
numbers. 
fuzzy_factorp2_factorise uses the powers of 2 to calculate the small primes (which allows it decode the secret message in 
secremessage.py and sfactorPFLLint uses a factorization engine i created from the Lucas-Lehmer Prime test. I modified the math 
of it to make it a factorization engine. Both work great. Other good featues of lars prime are 
random_powers_of_2_prime_finder(smallnum) to create primes which can be used to multiply together to test the engines. 
fuzzy_factorp2_factorise can factorize a few thousand Quintillion numbers near the powers of two that ECM cannot, so it will 
be the underpinning of the new engine. see: python3 secretmessage.py and awesomenumberswecanfactor.txt for more informtation. 
Try those number in any engine and only fuzzy factor can factor them. I hope to have the new repo up and running by end of 
July. 
Until then enjoy this engine, it's still quite fast and better than sympy's factorint and as far as i know the best 
factorization engine for python.

** UPDATE JUNE 21st 2020 **

COMING SOON A NEW REPO WITH ALPERTON ECM. CALLED SFACTORINT

Here is a test run of a factor with ALPERTON's ECM under ubuntu. I haven't got ALPERTONS calculator to compile under osx yet,
but hopefully soon. The new repo will be called sfactorint. It will be PIP installable. For now though here is a hint of what's to come:

Ok, under ubunutu i got the Alperton ECM Calculator to compile. I'm going to be changing
this to a new repo, that compiles and pip installs and you'll soon have Alperton's calculator
that works with python for fast, fast factorization. It can factor a 60 digit number in seconds.


import time  
start = time.time()  
fuzzy_factorp2_factorise(632459103267572196107100983820469021721602147490918660274601)  
end = time.time()  
print(end-start)  


From Stackoverflow: https://stackoverflow.com/questions/61467904/craking-long-rsa-keys-from-public-key-only/61468947

Attempting to factorise: 632459103267572196107100983820469021721602147490918660274601
[] 632459103267572196107100983820469021721602147490918660274601
Attempting  to factorise 632459103267572196107100983820469021721602147490918660274601 with POLLARD_BRENT
Attempting to factorise 632459103267572196107100983820469021721602147490918660274601 with Alperton ECM
Alperton ECM SIQS Success
[972033825117160941379425504503, 650655447295098801102272374367]
19.50670623779297  # Less than a minute

And a 70 digit number in about 10 minutes:

In [2]: fuzzy_factorp2_factorise(285687553733060960861788359216915958112970509139629258898595989142255132118344811)                                 
Attempting to factorise: 285687553733060960861788359216915958112970509139629258898595989142255132118344811
[] 285687553733060960861788359216915958112970509139629258898595989142255132118344811
Attempting  to factorise 285687553733060960861788359216915958112970509139629258898595989142255132118344811 with POLLARD_BRENT
Attempting to factorise 285687553733060960861788359216915958112970509139629258898595989142255132118344811 with Alperton ECM
Alperton ECM SIQS Success
[24216099512878670489356468845463535766497, 11797422354542516053581104136761693231563]
Out[2]: 
[24216099512878670489356468845463535766497,
 11797422354542516053581104136761693231563]

THIS IS NOT IN THE CURRENT REPO, I'M SHOWING MY PROGRESS FOR THE NEW REPO AND SHOWING WHAT"S COMING SOON. UNTIL THEN ENJOY THIS ENGINE AS IT"S QUITE GOOD EVEN WITHOUT APLERTONS ECM. 

** END JUNE 21st 2020 UPDATE **

** UPDATE JUNE 19th 2020 **

While working on https://stackoverflow.com/questions/62365336/how-do-researchers-manage-to-find-such-large-primes I
tweaked the math of the LucasLehmer test to be a factorization engine. I included a new file, findprimell.py, which can
be used by: from findprimell import *

Try to see it in action:
sfactorPFLLint(272727272727272727272727272727272727272727272727272727272727272727272727) 
or
sfactorPFLLint(2727272727272727272727272727272727272727272727272727272727272727272727)
or
sfactorPFLLint(2413383613260094712864723197651621285243771156746061239374222)

It can factor the numbers itself in seconds from: https://stackoverflow.com/questions/4078902/cracking-short-rsa-keys

** UPDATE JUNE 15th 2020 **

I added a factoring easter egg. As far as i know only fuzzy factor can factor that (N) number (from secretmessage.py, which 
I built for this demonstration purposes) in about 60 seconds, but you'll be able to in just nano seconds once you decode it's 
secret cipher by running the algorithm. It's cipher is a  message about factoring and security. Have fun running it and ponder 
what it means about it's security!I hope you enjoy this easter egg, This is the kind of stuff that i would expect to see in
coding contests so i thought i'd share it here.
To run, use: python3 secretmessage.py

** UPDATE JUNE 14th 2020 **

I added awesomenumberswecanfactor.txt so you can try out some awesomely large factors that work with the non SIQs non BRENT 
POLLARD Part of the engine. I'm working on a new SIQs engine which i hope will be much faster so keep watching here for 
updates.

** UDADATE # 2 JUNE 12th 2020 **

I made some speed adjustments to factorise.py's siqs_choose_nf_m function. I commented out the old code for reference
plesae open up an issues case if you find any issues. The speed increase is anywhere from 1x to 5x.

To use the code here and the new function fuzzy_factorp2_factorise(num) use:  from larsprime import *

** UDADATE JUNE 12th 2020 **

Added fuzzy_factorp2_factorise(num) which utilizes the factorise.py engine from skollman. It uses the SIQS algorthim that
is incuded in factorise.py for those interseted in using it outright. My engine is setup to factor faster by reducing
the numbers so you may find fuzzy_Factorp2_factorize much fast than factorise.py alone. If you use sympy's factorint()
you may be very intersted in utilizing this engine to factor numbers as it now implements factorise.py's SIQS engine, and
can factor numbers that other engines can't yet. My short term goal is to implement PSIQS from https://www.rieselprime.de/ziki/Self-initializing_quadratic_sieve so keep watching here for updates on my progress, I think
in 2-3 weeks i should have something implemented.
Here is the description and some sample output:

     fuzzy_factorp2_factorise utilizes the factorise.py siqs_factorise algorithim. With this utilization
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
     
     With the new speed increases you can factor a number like this very quickly:
     
     In [58]: fuzzy_factorp2_factorise(random.randrange(2**180-1, 2**181-1,2))                                                                                                         
     Attempting to factorise: 2402956925397989535742923204519510889236432671327589210309935
     [] 6994795072985254881578072698617348710426689191283535041
     Attempting POLLARD_BRENT
     POLLARD BRENT Success
     [22606210609]
     [22606210609] 309419176613372003712011984229202963028392849
     Attempting POLLARD_BRENT
     Attempting factorise.py SIQS
     *** Step 1/2: Finding smooth relations ***
     Target: 1050 relations at about 1 relation per second (sometimes faster) required
     *** Step 2/2: Linear Algebra ***
     Building matrix for linear algebra step...
     Finding perfect squares using matrix...
     Finding factors from perfect squares...
     SIQS: Prime factor found: 62014126350947
     SIQS: Prime factor found: 92825296488583
     factorise.py SIQS Success
     [22606210609, 62014126350947, 92825296488583, 53751458290435949]
     Out[58]: [5, 127, 541, 22606210609, 62014126350947, 92825296488583, 53751458290435949]

     You can utilize this rather than sympy's factorint if you looking for speed and factorizations it can't
     yet do. 

     In the future i plan to implment a faster SIQ's engine which should be faster so keep watching here for 
     updates.

     This update can reduce numbers less than 50 digits rather fast but is logrimically slow on larger numbers

     For exampele it an factor a 60 digit number like 632459103267572196107100983820469021721602147490918660274601  
     in about an hour to two depending on your machine and factor a 41 digit number like 
     12785407097419647710079782477202050848441 in a few seconds.
     
 I also included lgcdsuaring.py for college students learning about primes to show how to find prime numbers via
 squaring rather than square rooting. It's a different approach and thougth it may be beneficial for those learning
 about primes. And it can be used by importing with: from lgcdsquaring import *

** UPDATE JUNE 11th 2020 **

fuzzy_factorp2 can factor primes near the powers of two which https://www.alpertron.com.ar/ECM.HTM cannot. Here are 
some examples:

    In [120]: fuzzy_factorp2(184497489401772529385612327842172717039008268166646221893471402059821287234759868672175917131173661172843563441437060059660158104845032398976807920666283692562120150139178769612799511748636278282415866878160176201872937423527853931074825229289817028865471580173776186278979555862451026349435370470391893467266722922032787249350725439886913605740602813268082709089291886620453265863627853622790654286086062735867956228695923216412207146334637881780340999262197111486948956274586736276726312611856766256076847267559903222158449249866341641399320010499519737541399320826909413745916727741131212329962162913187524444374554898629627270424650904523568673612685732404643) 
    
    [10715086071862673209484250490600018105614048117055336074437503883703510511249361224931983788156958581275946729175531468251871452856923140435984577574698574803934567774824230985421074605062371141877954182153046474983581941267398767559165543946077062914571196477686542167660429831652624386837205668069673,
     17218479456385750618067377696052635483579924745448689921733236816400740691241745619397484537236046173286370919031961587788584927290816661024991609882728717344659503471655990880884679896520055123906467064419056526231345685268240569209892573766037966584735183775739433978714578587782701380797240772477647874555986712746271362892227516205318914435913511141036262891]
     
     
    You can build these like this: fuzzy_factor_p2(lars_next_prime(2**1000)*lars_next_prime(2**1200)) and you can plug the
    number into your favorite engine and not be able to factorize those primes, but fuzzy factor can. This only works for
    primes near the powers of two and was interesting enough for me to post about it. Once again, build primes near the
    powers of two like this: lars_next_prime(2**1000)*lars_next_prime(2**1200) and see that fuzzy_factorp2(num) can
    factor them but https://www.alpertron.com.ar/ECM.HTM cannot factor. This was cool to me so wanted to post about it. 
    Also give give the June 9th update a try, it works well on all numbers. I'll have a SIQS addition soon utilizing 
    factorise.py so that should help with factorizations as well. Thx.
    
** END JUNE 11th 2020 UPDATE **    

** UPDATE JUNE 9th 2020 **

Added fuzzy_factorp2_brent_pollard(num, returnwithpsuedoprimeresults=False)

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
   into PARI or ECM and they can factor the numbers faster than you can by using PARI and factorint to reduce just the
   2 ** 1200-1 itself.  PARI can't seem to factor 2 ** 1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2 ** 1200-1.
 
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number.

   What is *AMAZING* about fuzzy_factor. hhttps://pari.math.u-bordeaux.fr/gp.html cannot reduce 2 ** 1000-1, but using 
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
   into PARI or factorint and they can factor the numbers faster than you can by using PARI and factorint to reduce just the
   2 ** 1200-1 itself.  PARI can't seem to factor 2 ** 1200-1 after an hour run, so you can factor the number using fuzzy
   factor then further reduce the psuedoprimes which it indicates and get the complete factorization for 2 ** 1200-1.
    
   This module factors as best as it can. If a number is too slow for modular reduction, it gives the best possible
   psuedoprime as an answer. This helps get an idea for the factors of very large numbers. Numbers that return
   themselves are composed of very large primes that are to slow for modular reduction and until a faster modular
   reduction technique is found by me or others, Use https://www.alpertron.com.ar/ECM.HTM to further reduce the
   number.
   What is *AMAZING* about fuzzy_factor. https://pari.math.u-bordeaux.fr/gp.html cannot reduce 2 ** 1000-1, but using 
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
