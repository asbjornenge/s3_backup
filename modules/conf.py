import json,os
import ConfigParser
from collections import OrderedDict as odict
from bunch import Bunch

path2 = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/../backup.cfg'
config = ConfigParser.ConfigParser()
config.readfp(open(path2))

def bunchIt(d):
  for key in d.keys():
    i = d[key]
    if type(i) in [dict,odict]:
      d[key] = bunchIt(i)
  return Bunch(d)

all = bunchIt(config._sections)

