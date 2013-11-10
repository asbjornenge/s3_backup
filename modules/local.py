import os
from datetime import datetime as _date
from datetime import timedelta

## Utility methods
#

def delete_old(days, paths):
  ago  = _date.utcnow() - timedelta(days=int(days))
  all  = files_to_objects(files_in_paths(paths))
  objs = filterOlderThan(ago, all)
  [os.remove(o['path']) for o in objs]
  return {"delete":len(objs),"keep":len(all)-len(objs)}

## Functions
#

def files_in_paths(paths):
  joined = []
  for path in paths:
    for dp,dr,filenames in os.walk(path):
      for fn in filenames:
        joined.append('%s/%s' % (path,fn))
  return joined

def files_to_objects(files):
  objs = []
  for file in files:
    date = lastModified(file.split('tgz-')[1].split('.')[0])
    objs.append({"path":file,"last_modified":date})
  return objs

def lastModified(datestr):
  return _date.strptime(datestr, "%Y-%m-%d %H:%M:%S")

def filterOlderThan(date, items):
  return [i for i in items if i['last_modified'] < date]
