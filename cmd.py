#!/usr/bin/python -tt
# shell command line parsing using python

import sys
import subprocess

def getstatusoutput(cmd):
  """Return (status, output) of executing cmd in a shell."""
  """Should work on all platforms."""

  pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
  output = "".join(pipe.stdout.readlines())
  sts = pipe.returncode
  if sts is None: sts = 0
  return sts, output

def listdir(dir):
  """Execute shell command ls-l to dir"""
  cmd = 'ls -l ' + dir
  print "Command to run:", cmd
  (status, output) = getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(1)
  print output
  
def main():
  listdir(sys.argv[1])
    
if __name__ == '__main__':
  main()