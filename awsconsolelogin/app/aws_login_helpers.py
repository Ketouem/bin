from ConfigParser import RawConfigParser
import json
import os
import requests
import urllib

def fetch_profile_names():
    config = RawConfigParser()
    config.read(os.path.join(os.getenv('HOME'),'.aws/credentials'))
    return config.sections()

def build_federation_token_payload(useralias='bob'):
    policy = json.dumps({
        "Version":"2012-10-17",
        "Statement": [
            {
                "Sid":"s",
                "Effect":"Allow",
                "Action":"*",
                "Resource":"*"
            }
        ]
    })
    return { "Name": useralias, "Policy": policy }

def build_credentials_params(federation_token):
    credentials = federation_token['Credentials']
    return {
        'sessionId': credentials['AccessKeyId'],
        'sessionKey': credentials['SecretAccessKey'],
        'sessionToken': credentials['SessionToken']
    }

def fetch_aws_federation_signin_token(federation_token):
    credentials = federation_token['Credentials']
    url = ('https://signin.aws.amazon.com/federation'
           '?Action=getSigninToken&Session={0}')
    jsoncreds = json.dumps(build_credentials_params(federation_token))
    return requests.get(url.format(urllib.quote_plus(jsoncreds))) \
                  .json()['SigninToken']

def build_sign_in_url(signin_token):
    return ('https://signin.aws.amazon.com/federation'
            '?Action=login&Issuer=https://example.com'
            '&Destination=https://console.aws.amazon.com'
            '&SigninToken={0}').format(signin_token)
