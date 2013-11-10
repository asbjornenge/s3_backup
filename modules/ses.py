import boto.ses as ses
from conf import all as conf

## Utility methods
#

def connect(key,secret):
  return ses.connect_to_region(
    'us-east-1',
    aws_access_key_id=key, 
    aws_secret_access_key=secret)

def email_admins(conn,subject,body):
  conn.send_email(
    conf.email.sender,
    subject, 
    body,
    conf.email.admins.splitlines()[1:])
