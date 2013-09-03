from string import *

def countSubStringMatch(target, key):
    cnt = 0
    pos = target.find(key)
    while pos != -1:
        cnt += 1
        pos = target.find(key, pos+1)
    return cnt
    
def countSubStringMatchRecursive(target, key):
    pos = target.find(key)
    if pos == -1:
        return 0
    else:
        subtarget = target[pos+1:]
        return 1 + countSubStringMatchRecursive(subtarget, key)

        
def subStringMatchExact(target, key):
    pos = target.find(key)
    result = ()
    while pos != -1:
        result = result + (pos,)
        pos = target.find(key, pos+1)
    return result 
        

def constrainedMatchPair(firstMatch, secondMatch, length):
    """Return a tuple of all members (call it n) of the first tuple for which 
    there is an element in the second tuple (call it k) such that n+m+1 = k, 
    where m is the length of the first substring.

    Input: a tuple representing starting points for the first substring, 
           a tuple representing starting points for the second substring, 
           the length of the first substring.
           
    """
    results = ()
    for n in firstMatch:
        if (n + length + 1) in secondMatch:
            results += (n,)
    return results
    
def subStringMatchOneSub(target, key):
    """search for all locations of key in target, with one substitution
       a function written by MIT course staff"""
    allAnswers = ()
    for miss in range(0,len(key)):
        # miss picks location for missing element
        # key1 and key2 are substrings to match
        key1 = key[:miss]
        key2 = key[miss+1:]
        print 'breaking key',key,'into', "'"+key1+"',", "'"+key2+"'"
        print 'length of key1:', len(key1)
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
        match1 = subStringMatchExact(target,key1)
        match2 = subStringMatchExact(target,key2)
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
        filtered = constrainedMatchPair(match1,match2,len(key1))
        allAnswers = allAnswers + filtered
        print 'match1',match1
        print 'match2',match2
        print 'possible matches for', "'"+key1+"',", "'"+key2+"'", \
              'start at', filtered
    return allAnswers
        
def subStringMatchExactlyOneSub(target, key):
    exactMatches = subStringMatchExact(target, key)
    exact_and_oneSub_matches = subStringMatchOneSub(target, key)
    results = ()
    for n in exact_and_oneSub_matches:
        if n not in exactMatches:
            results += (n,)
    return results

def main():    
    target1 = 'atgacatgcacaagtatgcat'
    target2 = 'atgaatgcatggatgtaaatgcag'
    key10 = 'a'
    key11 = 'atg'
    key12 = 'atgc'
    key13 = 'atgca'
    
    # test countSubStringMatch
    if countSubStringMatch(target1, key10) == 8:
        print 'target1:', target1, 'key10:', key10, 'PASS!'
    else:
        print 'target1:', target1, 'key10:', key10, 'FAIL!'
        
    if countSubStringMatch(target1, key11) == 3:
        print 'target1:', target1, 'key11:', key11, 'PASS!'
    else:
        print 'target1:', target1, 'key11:', key11, 'FAIL!'
    
    if countSubStringMatch(target1, key12) == 2:
        print 'target1:', target1, 'key12:', key12, 'PASS!'
    else:
        print 'target1:', target1, 'key12:', key12, 'FAIL!'

    if countSubStringMatch(target1, key13) == 2:
        print 'target1:', target1, 'key13:', key13, 'PASS!'
    else:
        print 'target1:', target1, 'key13:', key13, 'FAIL!'
    
    # test countSubStringMatchRecursive    
    if countSubStringMatchRecursive(target2, key10) == 9:
        print 'target2:', target2, 'key10:', key10, 'PASS!'
    else:
        print 'target2:', target2, 'key10:', key10, 'FAIL!'
        
    if countSubStringMatchRecursive(target2, key11) == 5:
        print 'target2:', target2, 'key11:', key11, 'PASS!'
    else:
        print 'target2:', target2, 'key11:', key11, 'FAIL!'
    
    if countSubStringMatchRecursive(target2, key12) == 2:
        print 'target2:', target2, 'key12:', key12, 'PASS!'
    else:
        print 'target2:', target2, 'key12:', key12, 'FAIL!'

    if countSubStringMatchRecursive(target2, key13) == 2:
        print 'target2:', target2, 'key13:', key13, 'PASS!'
    else:
        print 'target2:', target2, 'key13:', key13, 'FAIL!'

    # test subStringMatchExact
    if subStringMatchExact(target1, key10) == (0, 3, 5, 9, 11, 12, 15, 19):
        print 'target1:', target1, 'key10:', key10, 'PASS!'
    else:
        print 'target1:', target1, 'key10:', key10, 'FAIL!'
        print subStringMatchExact(target1, key10)
        
    if subStringMatchExact(target1, key11) == (0, 5, 15):
        print 'target1:', target1, 'key11:', key11, 'PASS!'
    else:
        print 'target1:', target1, 'key11:', key11, 'FAIL!'

    if subStringMatchExact(target1, key12) == (5, 15):
        print 'target1:', target1, 'key12:', key12, 'PASS!'
    else:
        print 'target1:', target1, 'key12:', key12, 'FAIL!'

    if subStringMatchExact(target1, key13) == (5, 15):
        print 'target1:', target1, 'key13:', key13, 'PASS!'
    else:
        print 'target1:', target1, 'key13:', key13, 'FAIL!'

    # test constrainedMatchPair
    print subStringMatchOneSub(target1, key11)        
    print subStringMatchOneSub(target1, key12)        
    print subStringMatchOneSub(target1, key13)
    print subStringMatchOneSub(target2, key11)
    print subStringMatchOneSub(target2, key12)
    print subStringMatchOneSub(target2, key13)    
    
    # test subStringMatchExactlyOneSub
    print subStringMatchOneSub(target1, key12)        
    print subStringMatchExact(target1, key12)
    print subStringMatchExactlyOneSub(target1, key12)

if __name__ == '__main__':
    main()
