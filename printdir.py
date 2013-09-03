#!/usr/bin/python -tt

import sys
import os

def printdir(dir):
  """for every file in dir, print its name, immediate path, and full path"""
  filenames = os.listdir(dir)
  for filename in filenames:
    print filename
    path = os.path.join(dir, filename)
    print path
    print os.path.abspath(path)

def main():
  printdir(sys.argv[1])
    
if __name__ == '__main__':
  main()