### this program shows how to remove repeating vowels using regular expression

import re

s1 = 'cabaceo'
s2 = 'guangming lang'
s3 = 'caabaaceeoo'

# find all vowels
pat = r'[aeiou]' # matches a, e, i, o, or u
pat = re.compile(pat)

print pat.sub('{\g<0>}', s1) # \g<0> backreferences the substring matched by pat
print pat.sub('{\g<0>}', s2) 
print pat.sub('{\g<0>}', s3) 

# remove repeating vowels
pat = r'([aeiou])\1' # matches any vowel which is followed by itself again
pat = re.compile(pat)
pat.findall(s3)
matches = pat.finditer(s3)
for match in matches:
    match.group(0)
pat.sub(r'\1', s3) # \1 backreferences the vowel

# what if a vowel is repeated more than once?
s4 = 'caaaaaabaaaceeeoooo'
pat.sub(r'\1', s4)

pat = r'([aeiou])\1+' # matches any vowel which is followed by itself one or more times
pat = re.compile(pat)
pat.findall(s4)
matches = pat.finditer(s4)
for match in matches:
    match.group(0)
pat.sub(r'\1', s4) # \1 backreferences the vowel
 