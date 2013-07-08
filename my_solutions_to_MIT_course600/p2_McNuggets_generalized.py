## Generalize to arbitrary package sizes instead of 6,9,20

import sys

bestSoFar = 0     # variable that keeps track of largest number
                  # of McNuggets that cannot be bought in exact quantity
packages = (6,11,22)   # variable that contains package sizes
nums_can_buy = [] # list that keeps track of the number of McNuggets that can
                  # be bought
for n in range(1, 150):   # only search for solutions up to size 150
  cant_buy = True
  for a in range(n):
    for b in range(n):
      for c in range(n):
        if packages[0]*a + packages[1]*b + packages[2]*c == n:
          cant_buy = False
          break        
  if cant_buy: bestSoFar = n
  else: nums_can_buy.append(n)
  print n, bestSoFar, nums_can_buy
  
  if len(nums_can_buy) >= 6: 
    is_consecutive = True
    last_6_vals = nums_can_buy[-6:]
    pre = last_6_vals[0]
    del last_6_vals[0]
    for val in last_6_vals:
      if val == pre + 1:
        pre = val
      else:
        is_consecutive = False
    if is_consecutive:
      print "Largest number of McNuggets that cannot be bought in exact quantity: %d" %bestSoFar
      sys.exit(0)  # a clean exit without any problem/error  