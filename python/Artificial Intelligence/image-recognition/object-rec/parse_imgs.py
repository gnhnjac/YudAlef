from os import listdir
from os.path import isfile, join
import os

dirpath = os.path.dirname(os.path.realpath(__file__))
mypath = dirpath + '\\all_imgs\\'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in onlyfiles:
    try:
        data = ""
        with open(mypath + f, 'r') as fh:
            data = fh.read()
        os.remove(mypath + f)
    except Exception as e:
        continue