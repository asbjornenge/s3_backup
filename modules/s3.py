import time
from boto.s3.key import Key
from datetime import datetime as _date
from datetime import timedelta

## Utility methods
#

def download_latest(name, bucket, path):
  l = bucket.list()
  latest_key = filterDate('latest', filterName(name,l))
  download(latest_key, path)
  return latest_key

def delete_old(older_than_days,bucket):
  now    = _date.utcnow()
  delta  = timedelta(days=int(older_than_days))
  report = {"keep" : 0, "delete" : 0}
  for key in bucket.list():
    if now-lastModified(key) > delta:
      report['delete'] += 1
      bucket.delete_key(key_name=key.key)
    else:
      report['keep'] += 1
  return report

## Pure functions
#

def download(key,path):
  filePath = "%s/%s" % (path,key.name.replace('/','_'))
  key.get_contents_to_filename(filePath)

def list(bucketList, filters=None):
  for key in bucketList:
    print "%s || %s"%(key.last_modified,key.name)

def lastModified(key):
  return _date.strptime(key.last_modified[:19], "%Y-%m-%dT%H:%M:%S")

def filterName(name, bucketList):
  return [item for item in bucketList if name in item.name]

def filterDate(date, bucketList):
  if date == 'latest':
      date = _date.now()
  def compareKeyDate(x):
    return lastModified(x) - date
  # Using max here actually ties this function to it's current use 'latest'.
  return max(bucketList, key=compareKeyDate)

def upload(bucket, s3_name, local_path):
  k     = Key(bucket)
  k.key = s3_name
  k.set_contents_from_filename(local_path)
  return k

# for archive in archives:
#     k      = Key(bucket)
#     k.key  = 'th3db1.www.taghub.net/%s-%s' % (archive, str(datetime.datetime.utcnow()))
#     k.path = 'th3db1.www.taghub.net'

#     def percent_cb(complete, total):
#         sys.stdout.write('.')
#         sys.stdout.flush()
#     print "Sending %s to S3 bucket" % archive
#     k.set_contents_from_filename(root+archive, cb=percent_cb, num_cb=10)
#     print "%s has been sent successfully!" % archive
# print "Backup tasks complete!"
