'''
Documentation, License etc.

@package scan2pdf
'''

import sys
import getopt
import os.path


class Pages:
  def __init__(self):
    self.pagesFile = 'pages'
    
  def hasPagesFile(self):
    return os.path.isfile(self.pagesFile)
  
  def getPageValue(self):
    with open(self.pagesFile) as f:
      line = f.readline();
    return line
  
  def setPageValue(self,v):
    buf = "%d\n" % (v)
    f = open(self.pagesFile,'w')
    f.write(buf)
    f.close()
    return
  
  

def main():
  print "bla"  
  p = Pages()
  p.setPageValue(65)
  
  
if __name__ == "__main__":
  main()
  