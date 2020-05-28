# This is a non probabilistic primality test. It preforms fermat's test from the bitlength of the number down to 2. 
# It then uses my algorithim to determine whether a number is composed of small primes. 
# If the fermat tests fail, then a prime should be found using my algorithm in the numer itself. If not the number
# is prime. I created a pandas table to view to look at to show how this method works. It is non probabalistic and 
# works via algorithims which do not use randomness to reduce errors


#import numpy as np


def SieveOfEratosthenes(n):  
      
   # Create a boolean array "prime[0..n]" and initialize  
   #  all entries it as true. A value in prime[i] will  
   # finally be false if i is Not a prime, else true.  
   prime = [True for i in range(n+1)]  
   p = 2 
   while (p * p <= n):  
          
       # If prime[p] is not changed, then it is a prime  
       if (prime[p] == True):  
              
           # Update all multiples of p  
           for i in range(p * p, n+1, p):  
               prime[i] = False 
       p += 1 

   size = 0 
   for p in range(2, n+1):  
     if prime[p]: 
       size+=1 

   #vv = np.zeros(size, dtype='int64') 
   vv = []
   count = 0  
   # Print all prime numbers  
   for p in range(2, n+1):  
       if prime[p]:  
           #vv[count] = p  
           vv.append(p)
           count+=1 
   return vv 


def get_factor_lars_prime(hm, offset=-2):
     num = hm
     vv = []
     a = lars_find_prime(num, offset)
     if a[5] == 0:
       vv.append(a[1])
     elif a[5] != 0 and a[3] == hm:
       vv.append(a[3])
     elif a[5] == 2:
       if num % 2 == 0:
         vv.append(a[5])
       else:
         vv.append(a[3])
     elif a[5] == 3:
       if num % 2 == 0:
          vv.append(2)
       elif num % 3 == 0:
          vv.append(3)
       elif num % 5 == 0:
          vv.append(5)
       elif num % a[3] == 0:
          vv.append(a[3])
     else:
       vv.append(a[5])
     num = num // vv[-1]
     return vv

def larsprimetest(hm):
   if hm == 1:
      return False
   larstest = [-2, -1, 0, 1, 2]
   primereducer = SieveOfEratosthenes(hm.bit_length())
   primetest = 0
   for x in primereducer[0:3]:
     if hm == int(x):   
        return True
   for x in np.flip(primereducer):
     if  pow(int(x),hm-1,hm)%hm != 1:   
        return False
   for x in larstest:
     if get_factor_lars_prime(hm, x)[0] == hm:
        primetest += 1
   if primetest == 5:
        return True
   else:
        return False
   return True


def Xploder(s, iter=1):
  return ((s+1) << (iter))-1


def powers(hm, y):
   return hm%y

def find_prime_evens(hm, offset=-2):
   y = 3
   prevtemp = 3
   if larsprimetest(hm):
      print(f"{hm} is already prime")
      return hm
   count = 0
   while True:
     count += 1
     if y.bit_length() > hm.bit_length() -1:
       hm = hm**2
     j = powers(hm, y)
     temp = j
     if j != 1 and j != 0:
       temp = j
       temp = hm % temp   
       if temp == 0:
          prevtemp = temp
          break   
       while temp != 1 and temp != 0:
          prevtemp = temp
          temp = hm % temp
     if temp == 0:
       print("h: break")
       break
     y = Xploder(y) -offset
   return hm, j, y.bit_length(), y, temp, prevtemp, count

def lars_find_prime(hm, offset=-2):
   y = 3
   prevtemp = 3 
   count = 0
   while True:
     count += 1
     j = powers(hm, y)
     temp = j
     if j != 1 and j != 0:
       temp = j
       temp = hm % temp   
       if temp == 0:
          prevtemp = temp
          break   
       while temp != 1 and temp != 0:
          prevtemp = temp
          temp = hm % temp
     if temp == 0:
       break
     y = Xploder(y) -offset
   return hm, j, y.bit_length(), y, temp, prevtemp, count


def build_prime_number(hm):
   si = 1
   for x in range(len(hm)):
     si = si * hm[x]
   return si

def lars_next_prime(hm):
   if hm == 1:
      return 2
   if hm == 2:
      return 3
   if hm % 2 == 0:
      hm = hm + 1
   hm += 2
   while larsprimetest(hm) == False:
      hm += 2
   return hm
