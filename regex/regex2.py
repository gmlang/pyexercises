### this program demos the functionality of () and \1 as regular expressions 

import re

s = '''And the first one now will later be last
For the times they are a-changin'''

# .match matches from the beginning of the string, only return one matchObject
# .groups() => a tuple of matched items
# .group(0) => matched substring
# .group(1) => the 1st matched item specified by the 1st pair of parentheses in the pattern
# .group(2) => the 2nd matched item specified by the 2nd pair of parentheses in the pattern

pattern = r'(And)( )(the)'
re.compile(pattern).match(s).groups() # ('And', ' ', 'the')
re.compile(pattern).match(s).group(0) # 'And the'
re.compile(pattern).match(s).group(1) # 'And'
re.compile(pattern).match(s).group(2) # ' ' 
re.compile(pattern).match(s).group(3) # 'the'
re.compile(pattern).sub(r'\1', s) # 'And first one now will later be last\nFor the times they are a-changin'
re.compile(pattern).sub(r'\2', s) # ' first one now will later be last\nFor the times they are a-changin'
re.compile(pattern).sub(r'\3', s) # 'the first one now will later be last\nFor the times they are a-changin'

s3 = 'caabaaceeoo'

# .search matches anywhere within the string, only return one matchObject
pat = r'(a)(b)(a)'
re.search(pat, s1).groups() # ('a', 'b', 'a')
re.search(pat, s1).group(0) # 'aba'
re.search(pat, s1).group(1) # 'a'
re.search(pat, s1).group(2) # 'b'
re.search(pat, s1).group(3) # 'a'

pat = r'(a)'
re.search(pat, s1).groups() # ('a',)
re.search(pat, s1).group(0) # 'a'
re.search(pat, s1).group(1) # 'a'
re.search(pat, s1).group(2) # IndexError: no such group

pat = r'(aa)'
re.search(pat, s1).groups() # ('aa',)
re.search(pat, s1).group(0) # 'aa'
re.search(pat, s1).group(1) # 'aa'
re.search(pat, s1).group(2) # IndexError: no such group

pat = r'(a)\1' # this pattern is different from r'(aa)'
re.search(pat, s3).groups() # ('a',)
re.search(pat, s3).group(0) # 'aa'
re.search(pat, s3).group(1) # 'a'
re.search(pat, s3).group(2) # IndexError: no such group

pat = r'([aeiou])\1' # matches any vowel which is followed by itself again
pat = re.compile(pat)
matches = pat.finditer(s3)
for match in matches:
    match.group(0)
# 'aa'
# 'aa'
# 'ee'
# 'oo'    
pat.sub(r'\1', s3)

s4 = 'caaaaaabaaaceeeoooo'
matches = pat.finditer(s4)
for match in matches:
    match.group(0)

pat = r'([aeiou])\1+' # matches any vowel which is followed by itself one or more times
pat = re.compile(pat)
pat.findall(s4)
matches = pat.finditer(s4)
for match in matches:
    match.group(0)
# 'aaaaaa'
# 'aaa'
# 'eee'
# 'oooo'    
    
pat.sub(r'\1', s4) # \1 backreferences the vowel
 