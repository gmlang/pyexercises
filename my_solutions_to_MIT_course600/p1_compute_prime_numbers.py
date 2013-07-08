def print_primes(num):
  """Find and print the num_th prime number and all primes before it, excluding 2"""
  primes_cnt = 1 # 2 is the first prime
  n = 3
  while True:
    if primes_cnt == num:
      break
    else:
      is_prime = True
      for i in range(2, n): # check if n is prime
        if n % i == 0:
          is_prime = False    
      if is_prime:   # if n is prime
        primes_cnt += 1
        print "prime index:", primes_cnt, "value:", n     
      n += 2
  return None
  
# for sufficiently large n, the product of the primes less than n is 
# less than or equal to e**n and that as n grows, and the ratio of the product 
# of the primes to e**n gets close to 1 as n grows. Though the convergence is not monotonic.
# check this by taking log on both sides

def is_odd(n):
  """return True if n is odd; False if n is even"""
  if n % 2 == 0: return False
  else: return True

def is_prime(n):
  """return True if n is prime; False if n is not"""
  if is_odd(n):
    is_prime = True
    for i in range(2, n):
      if n % i == 0:
        is_prime = False
    return is_prime
  else:
    return False
    
def sum_log_primes(n):
  """Given any positive real number n, find the log of every prime < n,
     take their sum and divide the result by n. Print out n, sum of log of 
     primes < n, and the ratio.""" 
  from math import log, floor
  sum_log_primes = 0
  for num in range(2, int(floor(n))):
    if is_prime(num):
      sum_log_primes += log(num)
  ratio = sum_log_primes * 1.0 / n
  return n, sum_log_primes, ratio    
  
def main():
  large_nums = range(1000, 30000, 1000)
  for large_num in large_nums:
    print sum_log_primes(large_num)
    
if __name__ == '__main__':
  main()