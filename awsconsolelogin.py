#!/usr/bin/env python

import boto3
import flask
import ConfigParser
import json
import os
import urllib
import requests
import sys

useralias = 'bob'
app = flask.Flask(__name__)

@app.route('/login/<profile>')
def login(profile):
    session = boto3.session.Session(profile_name=profile)
    userarn = session.client('sts').get_caller_identity()['Arn']
    username = userarn.split('/')[-1]
    policies = session.client('iam').list_attached_user_policies(UserName=username)
    creds = session.client('sts').get_federation_token(
        Name = useralias,
        Policy='{\
            "Version":"2012-10-17",\
            "Statement":[{\
                "Sid":"s",\
                "Effect":"Allow",\
                "Action":"*",\
                "Resource":"*"}]}'
    )['Credentials']

    jsoncreds = '{{"sessionId":"{0}","sessionKey":"{1}","sessionToken":"{2}"}}'.format(
                                        creds['AccessKeyId'],
                                        creds['SecretAccessKey'],
                                        creds['SessionToken'])

    url = 'https://signin.aws.amazon.com/federation\
?Action=getSigninToken&Session='+urllib.quote_plus(jsoncreds)
    r = requests.get(url)
    url='https://signin.aws.amazon.com/federation\
?Action=login\
&Issuer=https%3A%2F%2Fexample.com\
&Destination=https%3A%2F%2Fconsole.aws.amazon.com%2F\
&SigninToken='+json.loads(r.text)['SigninToken']
    return flask.redirect(url,code='302')

@app.route("/")
def main():
    index = '<!DOCTYPE html><html lang="en"><body>'
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.getenv('HOME'),'.aws/credentials'))
    for profile in config.sections():
        index += '<a href="/login/{0}">{0}</a></br>'.format(profile)
    index += '</body></html>'
    return flask.render_template_string(index)

if __name__ == "__main__":
    app.run()

