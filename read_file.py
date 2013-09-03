#!/usr/bin/python -tt

import sys
import codecs # provides support for reading a unicode file

def cat_bytes(filename):
  """Read bytes file"""
  try:    
    f = open(filename, 'rU') # 'U' lets us ignore DOS line ending or unix line ending

    ############
    # choice 1 #
    ############
    # reads one line at a time 
    # has the nice quality that not all the file needs to fit in memory at one time
    # only works for text files, not binary files
    for line in f: 
      print line,
    
    ############
    # choice 2 #
    ############
    # # reads the whole file into memory and returns its contents as a list of its lines
    # lines = f.readlines() 
    # print lines

    ############
    # choice 3 #
    ############
    # # reads the whole file into a single string
    # text = f.read()
    # print text,
    
    f.close()
  except IOError:
    # print 'IO Error', filename
    raise ValueError("couldn't open " + filename)
    
def cat_unicode(filename):
  """Read unicode file"""
  try:    
    f = codecs.open(filename, 'rU', 'utf-8') # 'U' lets us ignore DOS line ending or unix line ending
    
    # # choice 1
    # for line in f:
      # print line,
      
    # # choice 2
    # lines = f.readlines()
    # print lines
    
    # choice 3
    text = f.read()
    print text,
    f.close()
    
  except IOError:
    # print 'IO Error', filename
    raise ValueError("couldn't open " + filename)
    
def main():
  for arg in sys.argv[1:]:
    cat_bytes(arg)
    # cat_unicode(arg)
    
if __name__ == '__main__':
    main()