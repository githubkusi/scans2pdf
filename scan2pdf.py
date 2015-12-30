'''
Documentation, License etc.

@package scan2pdf
'''

import sys
import getopt
import os.path
import os
import argparse

class PageControl:
  def __init__(self):
    self.pagesFile = 'pages'
    
  def hasPagesFile(self):
    return os.path.isfile(self.pagesFile)
  
  def getPageValue(self):
    with open(self.pagesFile) as f:
      line = f.readline()
    return int(line)
  
  def setPageValue(self,v):
    buf = "%d" % (v)
    f = open(self.pagesFile,'w')
    f.write(buf)
    f.close()
    return
  
  def rmPagesFile(self):
	os.remove(self.pagesFile)
  

class MockScan:
  def __init__(self):
    return 
  
  def scanToPdf(self,n,count):
    cmd = "cp tmp.pdf %s.%d.pdf" % (n, count)
    os.system(cmd)    
  
class Scan:
  def __init__(self):
    return

  def scanToJpg(self,n):
    os.system("hp-scan -o " + n)
    
  def convert(self,src,tar):
    os.system("convert -page a4 " + src + " " + tar)
	  
  def rm(self,n):
    os.system("rm " + n)    
  
  def scanToPdf(self,n,count):
    c = str(count)
    q="\""
    n_jpg = q + n + "." + c + ".jpg" + q
    n_pdf = q + n + "." + c + ".pdf" + q
    self.scanToJpg(n_jpg)
    self.convert(n_jpg,n_pdf)
    self.rm(n_jpg)
    
class PdfUnite:
  def __init__(self):
    return 
  
  def pdfunite(self,n):
    src = n + "*pdf"
    tar = n + ".pdf"
    os.system("pdfunite " + src + " " + tar)
    os.system("rm " + n + ".*.pdf")  
    
class Params:  
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
    
class MockParams:
  def __init__(self):
	self.name='mydoc'
	self.pageCount=1
	self.color=False
	
  def parseArgs(self):
	return	
	  
class Control:
  def __init__(self,p,s,pu):
	self.pageControl=p
	self.scan=s
	self.pdfunite=pu
	
  def run(self,name,pageCount,color):
        #name without suffix
	if self.pageControl.hasPagesFile():
	  #scanning in progress
	  pageCount=self.pageControl.getPageValue()
	else:
	  #new scanning starts
	  self.pageControl.setPageValue(pageCount)
	  
	self.scan.scanToPdf(name,pageCount)
	  
	if pageCount > 1:
	  #multipage scanning in progress, expecting more scans
	  self.pageControl.setPageValue(pageCount-1)
	else:
	  #last page was scanned: remove pagefile and unite pdfs
	  self.pageControl.rmPagesFile()
	  self.scan.pdfunite(name)
	  
	  
	return 
  

                  

def main():
  print(os.getcwd() + "\n")
  p = PageControl()
  #m = Params()
  m = MockParams()
  # s = Scan()
  s = MockScan()
  pu  = PdfUnite()
  c = Control(p,s,pu)
  
  m.parseArgs()
  c.run(m.name,m.pageCount,m.color)
  
  
  
  
  
if __name__ == "__main__":
  main()
  