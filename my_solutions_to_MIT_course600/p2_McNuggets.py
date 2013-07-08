# McDonald's sells Chicken McNuggets in packages of 6, 9 or 20 McNuggets. 
# Thus, it is possible, for example, to buy exactly 15 McNuggets (with one 
# package of 6 and a second package of 9), but it is not possible to buy exactly 
# 16 nuggets, since no non-negative integer combination of 6's, 9's and 20's 
# adds up to 16. To determine if it is possible to buy exactly n McNuggets, one 
# has to solve a Diophantine equation: find non-negative integer values 
# of a, b, and c, such that 6a + 9b + 20c = n.

# Theorem: If it is possible to buy x, x+1, ..., x+5 sets of McNuggets, 
# for some x, then it is possible to buy any number of McNuggets >= x, 
# given that McNuggets come in 6, 9 and 20 packs. Its proof is straightforward.

# Using this theorem, we can write an exhaustive search to find the largest 
# number of McNuggets that cannot be bought in exact quantity.

import sys

n = 1
nums_cant_buy = []
nums_can_buy = []

while True:
  cant_buy = True
  for a in range(n):
    for b in range(n):
      for c in range(n):
        if 6*a+9*b+20*c == n:
          cant_buy = False
          break        
  if cant_buy: nums_cant_buy.append(n)
  else: nums_can_buy.append(n)
  print n, nums_cant_buy, nums_can_buy
  
  # When found six consecutive values of n that in fact pass the test of having 
  # an exact solution, the last n that was appended to nums_cant_buy is 
  # the correct answer by the theorem.
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
      print "Largest number of McNuggets that cannot be bought in exact quantity: %d" %nums_cant_buy[-1]
      sys.exit(0)  # a clean exit without any problem/error
  # Don't forget to increment n by 1
  n += 1 

