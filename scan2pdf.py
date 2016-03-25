#!/usr/bin/python3

'''
Documentation, License etc.

@package scan2pdf
'''

import sys
import getopt
import os.path
import os
import argparse
import json


class PageValues(object):
    def __init__(self, j=None):
        if j is None:
            self.current = 1
            self.total = 1

        else:
            self.__dict__ = json.loads(j)

    def serialize(self):
        return json.dumps(self.__dict__)


class PageControl:
    def __init__(self):
        self.pagesFile = 'pages'

    def has_pages_file(self):
        return os.path.isfile(self.pagesFile)

    def get_page_values(self):
        with open(self.pagesFile) as f:
            js = f.readline()
        pv = PageValues(js)
        return pv

    def set_page_values(self, pv):
        buf = pv.serialize()
        f = open(self.pagesFile, 'w')
        f.write(buf)
        f.close()

    def rm_pages_file(self):
        if self.has_pages_file():
            os.remove(self.pagesFile)


class MockScan:
    def __init__(self):
        return

    @staticmethod
    def scan_to_pdf(n, _):
        cmd = "cp tmp.pdf " + n
        os.system(cmd)
        return 0


class Scan:
    def __init__(self):
        return

    @staticmethod
    def scan_to_jpg(n, color=False):
        c = {True: 'color', False: 'grey'}
        cmd = "hp-scan -m" + c[color] + " -o" + n
        ret = os.system(cmd)
        return ret

        # debug
        # os.system("cp tmp.jpg " + n)

    @staticmethod
    def convert(src, tar):
        os.system("convert -page a4 " + src + " " + tar)

    @staticmethod
    def rm(n):
        os.system("rm " + n)

    def scan_to_pdf(self, n, color=False):
        q = "\""
        n_jpg = q + n + ".jpg" + q
        n_pdf = q + n + q
        ret = self.scan_to_jpg(n_jpg, color)
        if ret == 0:
            self.convert(n_jpg, n_pdf)
            self.rm(n_jpg)

        return ret


class PdfUnite:
    def __init__(self):
        return

    @staticmethod
    def pdfunite(n):
        q = "\""
        src = q + n + q + ".*.pdf"
        tar = q + n + ".pdf" + q
        cmd = "pdfunite " + src + " " + tar
        os.system(cmd)
        os.system("rm " + q + n + q + ".*.pdf")


class Params:
    def __init__(self):
        [self.name, self.pageCount, self.color, self.rescan] = [None, None, None, None]

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Scan to a pdf document')
        group1 = parser.add_mutually_exclusive_group()
        group1.add_argument('-n', '--name', metavar='<filename>', type=str, help='an integer for the accumulator')
        group1.add_argument('filename', nargs='?')
        group2 = parser.add_mutually_exclusive_group()
        group2.add_argument('-c', '--count', metavar='<count>', type=int, help='number of pages to be scanned')
        group2.add_argument('pagecount', metavar='<count>', type=int, help='number of pages to be scanned', nargs='?')
        parser.add_argument('--color', dest='color', action='store_true', help='color instead of black & white')
        parser.add_argument('-r', '--rescan', dest='rescan', action='store_true', help='rescan previous page')

        args = parser.parse_args()

        self.name = args.name or args.filename
        self.pageCount = args.count or args.pagecount or 1
        self.color = args.color
        self.rescan = args.rescan


class MockParams:
    def __init__(self):
        self.name = 'mydoc'
        self.pageCount = 2
        self.color = True
        self.rescan = False

    @staticmethod
    def parse_args():
        return


class Control:
    def __init__(self, p, s, pu):
        self.pageControl = p
        self.scan = s
        self.pdfunite = pu

    @staticmethod
    def get_cur_pdf_name(name, count):
        return "%s.%d.pdf" % (name, count)

    def run(self, name, page_count, color, rescan):
        # name without suffix
        if self.pageControl.has_pages_file():
            # scanning in progress

            pv = self.pageControl.get_page_values()
            assert pv.current > 1

            if rescan:
                pv.current -= 1
                print("rescan again page %d" % pv.current)

                # TODO
                # test for inconsistency between pageCount,name,color or even forbid params

        else:
            # new scanning starts
            pv = PageValues()
            pv.total = page_count
            pv.name = name
            pv.color = color

        cur_pdf_name = self.get_cur_pdf_name(pv.name, pv.current)
        if self.scan.scan_to_pdf(cur_pdf_name, pv.color) > 0:
            print("abort scan2pdf due to scanning error")
            sys.exit(-1)

        if pv.current < pv.total:
            # multipage scanning in progress, expecting more scans
            print("Page %d of %d scanned" % (pv.current, pv.total))
            pv.current += 1
            self.pageControl.set_page_values(pv)

        else:
            # last page was scanned: remove pagefile if any and unite pdfs
            print("Last page was scanned, unite the %d scans" % pv.total)
            self.pageControl.rm_pages_file()
            self.pdfunite.pdfunite(pv.name)


def main():
    p = PageControl()
    m = Params()
    # m = MockParams()
    s = Scan()
    # s = MockScan()
    pu = PdfUnite()
    c = Control(p, s, pu)

    m.parse_args()
    c.run(m.name, m.pageCount, m.color, m.rescan)


if __name__ == "__main__":
    main()
