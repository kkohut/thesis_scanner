from setuptools import setup

setup(
    name='thesis_scanner',
    version='0.9',
    description='A program that recognizes bachelor and master theses',
    long_description='This application automatically scans and analyzes cover sheets of bachelor and master thesis in ' \
                'order to check if it was handed in in time.',
    packages=['thesis_scanner'],
    install_requires=['opencv-python', 'pytesseract', 'pillow', 'textdistance', 'imutils', 'numpy', 'datetime',
                      'pandas']
)