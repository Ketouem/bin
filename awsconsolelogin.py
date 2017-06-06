#!/usr/bin/env python

import boto3
import json
import urllib
import requests
import sys

session = boto3.session.Session(profile_name='shaiou')
userarn = session.client('sts').get_caller_identity()['Arn']
username = userarn.split('/')[-1]
policies = session.client('iam').list_attached_user_policies(UserName=username)
creds = session.client('sts').get_federation_token(
    Name = 'bob',
    Policy='{"Version":"2012-10-17","Statement":[{"Sid":"s","Effect":"Allow","Action":"*","Resource":"*"}]}'
)['Credentials']

jsoncreds = '{{"sessionId":"{0}","sessionKey":"{1}","sessionToken":"{2}"}}'.format(
                                    creds['AccessKeyId'],
                                    creds['SecretAccessKey'],
                                    creds['SessionToken'])


url = 'https://signin.aws.amazon.com/federation\
?Action=getSigninToken&Session='+urllib.quote_plus(jsoncreds)
print url
r = requests.get(url)
url='https://signin.aws.amazon.com/federation\
?Action=login\
&Issuer=https%3A%2F%2Fexample.com\
&Destination=https%3A%2F%2Fconsole.aws.amazon.com%2F\
&SigninToken='+json.loads(r.text)['SigninToken']
print url
