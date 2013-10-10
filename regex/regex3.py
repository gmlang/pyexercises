### this program demos how \b, \w, \s, work in regular expressions
### it also shows how to remove repeating words in a string

import re
s = 'happiness is is is is a warm warm warm gun gun.'

# demo \b, which matches word boundaries (0-width)
pat1 = r'\b'
print re.compile(pat1).sub('{\g<0>}', s) # '{}happiness{} {}is{} {}is{} {}is{} {}is{} {}a{} {}warm{} {}warm{} {}warm{} {}gun{} {}gun{}.'

# demo \w, which matches any alphanumeric character, same as [a-zA-Z0-9_]
pat2 = r'\b\w+\b'
print re.compile(pat2).sub('{\g<0>}', s) # '{happiness} {is} {is} {is} {is} {a} {warm} {warm} {warm} {gun} {gun}.'

# demo \s, which matches any whitespace character, same as [ \t\n\r\f\v]
pat3 = r'\s*' # matches 0 or more whitespaces
print re.compile(pat3).sub('{\g<0>}', s) # '{}h{}a{}p{}p{}i{}n{}e{}s{}s{ }i{}s{ }i{}s{ }i{}s{ }i{}s{ }a{ }w{}a{}r{}m{ }w{}a{}r{}m{ }w{}a{}r{}m{ }g{}u{}n{ }g{}u{}n{}.{}'

# remove repeating words
pat = r'(\b\w+\b\s*)\1+' # or equivalently, pat = r'(\b\w+)\s+\1+'
pat = re.compile(pat)
print pat.sub(r'\1', s) # 'happiness is a warm gun gun.'

s = s.replace('.', ' ')
print s # 'happiness is is is is a warm warm warm gun gun '
s_deduped = pat.sub(r'\1', s)
print s_deduped # 'happiness is a warm gun '
print re.sub(r' $', r'.', s_deduped) # 'happiness is a warm gun.'







