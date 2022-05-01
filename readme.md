# Scans2pdf
CLI tool to scan multiple pages and combine them into one pdf. Support for OCR


# Usage
    
    $ scans2pdf -h
    usage: scans2pdf [-h] [-n <filename>] [-c <count>] [--color] [-r] [-f] [-L] [-t] [-l] [-o] [filename] [<count>]
    
    Scan to a pdf document
    
    positional arguments:
      filename
      <count>               number of pages to be scanned

    optional arguments:
      -h, --help            show this help message and exit
      -n <filename>, --name <filename>
                            an integer for the accumulator
      -c <count>, --count <count>
                            number of pages to be scanned
      --color               color instead of black & white
      -r, --rescan          rescan previous page
      -f, --finish          finish and start merge even if more pages are expected
      -L, --last            merge pages after scan even if more pages were specified
      -t, --append-today    append today's date as suffix in the form -YYYY-MM-DD
      -l, --landscape       rotate this page from portrait to landscape (clockwise)
      -o, --no-ocr          skip tesseract OCR (text recognition)


# Installation
Install [pipx](https://pypa.github.io/pipx)



    git clone https://github.com/githubkusi/scans2pdf.git
    pipx install scans2pdf

# Dependencies
Install a sane backend containing the command ```scanimage```, eg



    zypper install sane-backends

Install tesseract with your preferred language, eg.



    zypper install tesseract-ocr tesseract-ocr-traineddata-german



