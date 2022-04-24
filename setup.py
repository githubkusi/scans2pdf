from setuptools import setup, find_packages

setup(
    name='scans2pdf',
    version='0.1',
    packages=find_packages(),
    url='',
    license='GPL',
    author='Markus Leuthold',
    author_email='github@titlis.org',
    description='Scan multiple pages and unite them to a pdf',
    entry_points={"console_scripts": ["scans2pdf=scans2pdf.main:main"]}
)
