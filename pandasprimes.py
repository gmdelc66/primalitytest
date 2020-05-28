# This creates a pandas table to show how this primality test works
# It is useful for seeing how the determination of primes are made
# The first numbers are prime, and the second numbers are an offset
# from the prime numbers. The default offset is 12 away.

import pandas as pd
import numpy as np

try:
  del primetable2
except:
  next

jnum=252587
j=jnum
larstest = [-2, -1, 0, 1, 2]
lsize=100


primetable2=pd.DataFrame(dtype='int64')
primetable2['pnum'] = np.zeros(lsize, 'int64')
primetable2['pprime'] = np.zeros(lsize, 'bool')


primetable2['pnumpow'] = np.zeros(lsize, 'int16')
primetable2['pf'] = np.zeros(lsize, 'int64')

primetable2['num'] = np.zeros(lsize, 'int64')
primetable2['nprime'] = np.zeros(lsize, 'bool')

primetable2['numpow'] = np.zeros(lsize, 'int16')

primetable2['nf'] = np.zeros(lsize, 'int64')

for x in range(0,lsize):
   primereducer = SieveOfEratosthenes(j.bit_length())
   primetest = 0
   j = lars_next_prime(j)
   primetable2.loc[x, ('pnum')] = j

   if larsprimetest(int(primetable2.loc[x, ('pnum')])) == True:
       primetable2.loc[x, ('pprime')] = True
   else:
       primetable2.loc[x, ('pprime')] = False

   for xx in np.flip(primereducer):
      if pow(int(xx),int(primetable2.loc[x, ('pnum')])-1,int(primetable2.loc[x, ('pnum')]))%int(primetable2.loc[x, ('pnum')]) != 1:  
         primetable2.loc[x, ('pnumpow')] = int(xx)
         break
      else:
         #print(xx)
         primetable2.loc[x, ('pnumpow')] = 0

   for xx in larstest:
     if get_factor_lars_prime(int(primetable2.loc[x, ('pnum')]), xx)[0] == int(primetable2.loc[x, ('pnum')]):
        primetest += 1
   if primetest == 5:
     primetable2.loc[x, ('pf')] = int(primetable2.loc[x, ('pnum')])


j=jnum
offset = 12

for x in range(0,lsize):
   primereducer = SieveOfEratosthenes(j.bit_length())
   primetest = 0
   j = lars_next_prime(j)
   primetable2.loc[x, ('num')] = j + offset

   if larsprimetest(int(primetable2.loc[x, ('num')])) == True:
       primetable2.loc[x, ('nprime')] = True
   else:
       primetable2.loc[x, ('nprime')] = False

   for xx in np.flip(primereducer):
      if pow(int(xx),int(primetable2.loc[x, ('num')])-1,int(primetable2.loc[x, ('num')]))%int(primetable2.loc[x, ('num')]) != 1:  
         primetable2.loc[x, ('numpow')] = int(xx)
         break
      else:
         #print(xx)
         primetable2.loc[x, ('numpow')] = 0

   for xx in larstest:
     if get_factor_lars_prime(int(primetable2.loc[x, ('num')]), xx)[0] != j:
        primetable2.loc[x, ('nf')] = get_factor_lars_prime(int(primetable2.loc[x, ('num')]), xx)[0]


