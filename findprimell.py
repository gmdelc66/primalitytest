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
    
    In [11]:  sfactorPFLLint(2727272727272727272727272727272727272727272727272727272727272727272727)                                                                                          
    Attempting to factorise 2727272727272727272727272727272727272727272727272727272727272727272727 with PrimeFinderLucasLehmer
    Attempting to factorise 909090909090909090909090909090909090909090909090909090909090909090909 with PrimeFinderLucasLehmer
    Attempting to factorise 303030303030303030303030303030303030303030303030303030303030303030303 with PrimeFinderLucasLehmer
    Attempting to factorise 101010101010101010101010101010101010101010101010101010101010101010101 with PrimeFinderLucasLehmer
    Attempting to factorise 2463661000246366100024636610002463661000246366100024636610002463661 with PrimeFinderLucasLehmer
    Attempting to factorise 34699450707695297183445586056372727619721779804225699107183133291 with PrimeFinderLucasLehmer
    Attempting to factorise 145185986224666515411906217809090910542768953155756063209971269 with PrimeFinderLucasLehmer
    Attempting to factorise 535741646585485296722901172727272732630143738582125694501739 with PrimeFinderLucasLehmer
    Attempting to factorise 115238039704341857759281818181818182970562215225236759411 with PrimeFinderLucasLehmer
    Attempting to factorise 12676057606901535338167618323816761959142252252253521 with PrimeFinderLucasLehmer
    Attempting to factorise 102597774254368927310726892731072690299085011471 with PrimeFinderLucasLehmer
    Attempting to factorise 112857540394051780636621518342028125126181 with PrimeFinderLucasLehmer
    Attempting to factorise 27210514393617801994618420840059911 with PrimeFinderLucasLehmer
    PrimeFinderLucasLehmer did not succeed
    Attempting to factorise 27210514393617801994618420840059911 with BrentPollard
    Brent Pollard did not succeed
    Attempting to factorise 27210514393617801994618420840059911 with factorise.py SIQS
    *** Step 1/2: Finding smooth relations ***
    Target: 315 relations at about 1 relation per second (sometimes faster) required
    *** Step 2/2: Linear Algebra ***
    Building matrix for linear algebra step...
    Finding perfect squares using matrix...
    Finding factors from perfect squares...
    SIQS: Prime factor found: 102598800232111471
    Out[11]: 
    [3, 3, 3, 41, 71, 239, 271, 4649, 9091, 123551, 909091, 4147571, 102598800232111471, 265212793249617641]
    
    In [47]: sfactorPFLLint(2413383613260094712864723197651621285243771156746061239)                                                                                                          
    Attempting to factorise 2413383613260094712864723197651621285243771156746061239 with PrimeFinderLucasLehmer
    Attempting to factorise 804461204420031570954907732550540428414590385582020413 with PrimeFinderLucasLehmer
    Attempting to factorise 9306477301512379206104831417389206839515859205493 with PrimeFinderLucasLehmer
    Attempting to factorise 327358588114684976823132414695881207200951817 with PrimeFinderLucasLehmer
    PrimeFinderLucasLehmer did not succeed
    Attempting to factorise 327358588114684976823132414695881207200951817 with BrentPollard
    Brent Pollard did not succeed
    Attempting to factorise 327358588114684976823132414695881207200951817 with factorise.py SIQS
    *** Step 1/2: Finding smooth relations ***
    Target: 1050 relations at about 1 relation per second (sometimes faster) required
    *** Step 2/2: Linear Algebra ***
    Building matrix for linear algebra step...
    Finding perfect squares using matrix...
    Finding factors from perfect squares...
    SIQS: Prime factor found: 4765792358854260848501601750691
    Out[47]: [3, 86441, 28429, 4765792358854260848501601750691, 68689225938787]

    In [197]: sfactorPFLLint(2413383613260094712864723197651621285243771156746061239374223)                                                                                                   
    Attempting to factorise 2413383613260094712864723197651621285243771156746061239374223 with PrimeFinderLucasLehmer
    Attempting to factorise 804461204420031570954907732550540428414590385582020413124741 with PrimeFinderLucasLehmer
    Attempting to factorise 268153734806677190318302577516846809471530128527340137708247 with PrimeFinderLucasLehmer
    Attempting to factorise 4544978556045376107089874195200793380873392008937968435733 with PrimeFinderLucasLehmer
    PrimeFinderLucasLehmer did not succeed
    Attempting to factorise 4544978556045376107089874195200793380873392008937968435733 with BrentPollard
    Attempting to factorise 796399618224964259464868482209503918825625160693519 with BrentPollard
    Attempting to factorise 2388450839323369523897103205168402389929 with BrentPollard
    Brent Pollard did not succeed
    Attempting to factorise 2388450839323369523897103205168402389929 with factorise.py SIQS
    *** Step 1/2: Finding smooth relations ***
    Target: 525 relations at about 1 relation per second (sometimes faster) required
    *** Step 2/2: Linear Algebra ***
    Building matrix for linear algebra step...
    Finding perfect squares using matrix...
    Finding factors from perfect squares...
    SIQS: Prime factor found: 4853249826931786679227
    Out[197]: [3, 3, 59, 5706907, 333437726711, 4853249826931786679227, 492134327408680427]

"""
    
from larsprime import *

def sfactorPFLLint(hm):
  vv = []
  nomorePFLL = False
  nomoreBP = False
  nomoreSIQS = False
  while True:
   if larsprimetest(hm) == True or hm == 1:
      vv.append(hm)
      break
   if nomorePFLL == False:
     prime = sfactorintPFLL(hm)
     if prime != False:
       hm = hm//prime
       vv.append(prime)
       continue
     else: 
       nomorePFLL = True
       if larsprimetest(hm):
         vv.append(hm)
         break
       continue
   if nomoreBP == False:
     print(f"Attempting to factorise {hm} with BrentPollard")
     prime = pollard_brent_lars_opt(hm)
     if prime != hm:
        hm = hm//prime
        vv.append(prime)
        continue
     else:
        print(f"Brent Pollard did not succeed")
        nomoreBP = True
        if larsprimetest(hm) == True:
           vv.append(hm)
           break
        continue
   if nomoreSIQS == False:
     print(f"Attempting to factorise {hm} with factorise.py SIQS")
     prime = siqs_factorise(hm)
     vv.extend(prime)
     for xx in prime:
        hm = hm//xx
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
