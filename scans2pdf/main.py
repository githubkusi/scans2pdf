import sys
import getopt
import os.path
import os
import argparse
import json
import time


class PageValues(object):
    """
    States of pages

    Properties
    - current: 1-indexed value of next scan (not the # of already performed scans)
    - total:   total amount of expected scans
    """
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


class Scan:
    def __init__(self):
        return

    @staticmethod
    def scan_to_jpg(n, color=False, resolution=300):
        c = {True: 'Color', False: 'Gray'}
        cmd = "scanimage -p --resolution " + resolution + " --mode " + c[color] + " --format=jpeg > " + n
        ret = os.system(cmd)
        return ret

        # debug
        # os.system("cp tmp.jpg " + n)

    @staticmethod
    def convert(src, tar):
        # This solution doesn't have the strange 72dpi thing, but results in a
        # "Missing 'endstream' or incorrect stream length" during pdfunite
        # cmd = "magick " + src + " pdf:- | pdfjam --paper a4paper --outfile " + tar

        cmd = "magick -page a4 -density 72 " + src + " " + tar
        print(cmd)
        os.system(cmd)

    @staticmethod
    def rotate(src):
        os.system(f'pdftk "{src}" cat 1-endright output tmp.pdf')
        os.system(f'mv tmp.pdf "{src}"')

    @staticmethod
    def rm(n):
        os.system("rm " + n)

    def scan_to_pdf(self, n, color, resolution):
        q = "\""
        n_jpg = q + n + ".jpg" + q
        n_pdf = q + n + q
        ret = self.scan_to_jpg(n_jpg, color, resolution)
        if ret == 0:
            self.convert(n_jpg, n_pdf)
            self.rm(n_jpg)

        return ret


class MockScan(Scan):
    @staticmethod
    def scan_to_pdf(n, _):
        cmd = f'cp test/sample.pdf "{n}"'
        os.system(cmd)
        return 0


def ocr_pdf(filename):
    # TODO Check presence of folder $TESSDATA_PREFIX
    #      or a proper output of tesseract --list-langs
    # TODO Make language configurable

    # Opencl support triggers generation of the profile file. Unfortunately, OpenSuseTW builds tesseract with --enable-opencl, which is a bad idea.
    # This hack can be removed once https://bugzilla.opensuse.org/show_bug.cgi?id=1213370 is solved
    # Trigger creation of tesseract_opencl_profile_devices.dat. Since dummy is not available, tesseract stops after profile generation
    os.system("tesseract dummy dummy")


    cmd = f"ocrmypdf -l deu \"{filename}\" \"{filename}\""
    print(cmd)
    ret = os.system(cmd)

    # cleanup hack
    fn_hack_profile = "tesseract_opencl_profile_devices.dat"
    if os.path.exists(fn_hack_profile):
        os.remove(fn_hack_profile)

    fn_hack_dummy = "dummy.txt"
    if os.path.exists(fn_hack_dummy):
        os.remove(fn_hack_dummy)


class PdfUnite:
    def __init__(self):
        return

    @staticmethod
    def pdfunite(n):
        q = "\""
        src = q + n + q + ".*.pdf"
        tar = q + n + ".pdf" + q
        cmd = "pdfunite " + src + " " + tar
        print(cmd)
        os.system(cmd)
        cmd_remove = "rm " + q + n + q + ".*.pdf"
        print(cmd_remove)
        os.system(cmd_remove)


class Params:
    def __init__(self):
        [self.name, self.pageCount, self.color, self.rescan, self.finish, self.appendToday, self.landscape, self.last_scan, self.ocr, self.resolution] \
            = [None, None, None, None, None, None, None, None, None, None]

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Scan to a pdf document')
        group1 = parser.add_mutually_exclusive_group()
        group1.add_argument('-n', '--name', metavar='<filename>', type=str, help='an integer for the accumulator')
        group1.add_argument('filename', nargs='?')
        group2 = parser.add_mutually_exclusive_group()
        group2.add_argument('-c', '--count', metavar='<count>', type=int, help='number of pages to be scanned')
        group2.add_argument('page_count', metavar='<count>', type=int, help='number of pages to be scanned', nargs='?')
        parser.add_argument('--color', dest='color', action='store_true', help='color instead of black & white')
        parser.add_argument('-r', '--rescan', dest='rescan', action='store_true', help='rescan previous page')
        parser.add_argument('-f', '--finish', dest='finish', action='store_true',
                            help='finish and start merge even if more pages are expected')
        parser.add_argument('-L', '--last', dest='last_scan', action='store_true',
                            help='merge pages after scan even if more pages were specified')
        parser.add_argument('-t', '--append-today', dest='append_today', action='store_true',
                            help='append today\'s date as suffix in the form -YYYY-MM-DD')
        parser.add_argument('-l', '--landscape', dest='landscape', action='store_true',
                            help='rotate this page from portrait to landscape (clockwise)')
        parser.add_argument('-o', '--no-ocr', dest='ocr', action='store_false',
                            help='skip tesseract OCR (text recognition)')
        parser.add_argument('--resolution', dest='resolution', type=str, default="300",
                            help='resolution in dpi (default 300)')

        args = parser.parse_args()

        self.name = args.name or args.filename
        self.pageCount = args.count or args.page_count or 1
        self.color = args.color
        self.rescan = args.rescan
        self.finish = args.finish
        self.last_scan = args.last_scan
        self.appendToday = args.append_today
        self.landscape = args.landscape
        self.ocr = args.ocr
        self.resolution = args.resolution

        if self.name is None and self.rescan is not True and self.finish is not True:
            parser.print_help()
            parser.error('Specify filename')


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
        return '{:s}.{:02d}.pdf'.format(name, count)

    @staticmethod
    def append_today(name):
        suffix = time.strftime("%Y-%m-%d")
        return name + '-' + suffix

    def run(self, name, page_count, color, rescan, finish, last_scan, append_today, landscape, ocr, resolution):
        # Parameter description
        #   name: without suffix ".pdf"

        if self.pageControl.has_pages_file():
            # scanning in progress

            pv = self.pageControl.get_page_values()
            assert pv.current > 1

            if finish:
                # start merge even if more files are expected
                print("Finish and unite {:d} of {:d} expected scans".format(pv.current - 1, pv.total))
                self.finish_job(pv.name, ocr)
                sys.exit(0)

            if rescan:
                pv.current -= 1
                print("rescan again page %d" % pv.current)

                # TODO
                # test for inconsistency between pageCount,name,color or even forbid params

        else:
            # new scanning starts

            # determine filename
            if append_today:
                name = self.append_today(name)

            pv = PageValues()
            pv.total = page_count
            pv.name = name
            pv.color = color

        assert not finish, "cannot finish when no scanning is in progress"

        cur_pdf_name = self.get_cur_pdf_name(pv.name, pv.current)
        if self.scan.scan_to_pdf(cur_pdf_name, pv.color, resolution) > 0:
            print("abort scan2pdf due to scanning error")
            sys.exit(-1)

        if landscape:
            self.scan.rotate(cur_pdf_name)

        if last_scan:
            print(f"Last page was scanned, unite {pv.current} of {pv.total} specified scans")
            self.finish_job(pv.name, ocr)
            return

        if pv.current < pv.total:
            # multi-page scanning in progress, expecting more scans
            print("Page %d of %d scanned" % (pv.current, pv.total))
            pv.current += 1
            self.pageControl.set_page_values(pv)

        else:
            # last page was scanned: remove pagefile if any and unite pdfs
            print("Last page was scanned, unite the %d scans" % pv.total)
            self.finish_job(pv.name, ocr)

    def finish_job(self, name, ocr):
        self.pageControl.rm_pages_file()
        self.pdfunite.pdfunite(name)

        # run text recognition
        if ocr:
            print("Run text recognition")
            ocr_pdf(name + ".pdf")


def main():
    p = PageControl()
    m = Params()
    # m = MockParams()

    if 'S2P_MOCKED_SCAN' in os.environ:
        s = MockScan()
    else:
        s = Scan()

    pu = PdfUnite()
    c = Control(p, s, pu)

    m.parse_args()
    c.run(m.name, m.pageCount, m.color, m.rescan, m.finish, m.last_scan, m.appendToday, m.landscape, m.ocr, m.resolution)


if __name__ == "__main__":
    main()
