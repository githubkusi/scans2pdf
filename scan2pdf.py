'''
Documentation, License etc.

@package scan2pdf
'''

import sys
import getopt
import os.path
import os
import argparse

class PageCount:
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
  
class Scan:
  def __init__(self):
    return

  def scanToJpg(self,n):
    os.system("hp-scan -o " + n)
    
  def convert(self,src,tar):
    os.system("convert -page a4 " + src + " " + tar)
    
  def rm(self,n):
    os.system("rm " + n)
  
  def scanToPdf(self,n):
    q="\""
    n_jpg = q + n + ".jpg" + q
    n_pdf = q + n + ".pdf" + q
    self.scanToJpg(n_jpg)
    self.convert(n_jpg,n_pdf)
    self.rm(n_jpg)
    
class Main:  

  def parseArgs(self):
    parser = argparse.ArgumentParser(description='Scan to a pdf document')
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-n','--name', metavar='<filename>', type=str, help='an integer for the accumulator')
    group1.add_argument('filename',nargs='?')
    group2 = parser.add_mutually_exclusive_group()  
    group2.add_argument('-c','--count', metavar='<count>', type=int, help='number of pages to be scanned')
    group2.add_argument('pagecount', metavar='<count>', type=int, help='number of pages to be scanned',nargs='?')
    parser.add_argument('--color',dest='color', action='store_true', help='color instead of black & white')

    args = parser.parse_args()
    
    self.name = args.name or args.filename
    self.pageCount = args.count or args.pagecount or 1
    self.color = args.color
    print self.name
    print self.pageCount
    print self.color
	  
      
    
    

def main():
  p = PageCount()
  m = Main()
  m.parseArgs()
  
  
  
if __name__ == "__main__":
  main()
  