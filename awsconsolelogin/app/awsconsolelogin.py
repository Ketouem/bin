import boto3
from flask import Blueprint, redirect, render_template
import urllib
import requests

from aws_login_helpers import (
    build_federation_token_payload, fetch_aws_federation_signin_token,
    build_sign_in_url, fetch_profile_names
)

consolelogin_blueprint = Blueprint('consolelogin', __name__)

@consolelogin_blueprint.route('/login/<profile>')
def login(profile):
    session = boto3.session.Session(profile_name=profile)
    userarn = session.client('sts').get_caller_identity()['Arn']
    username = userarn.split('/')[-1]
    policies = session.client('iam') \
                      .list_attached_user_policies(UserName=username)
    federation_token = session.client('sts') \
                       .get_federation_token(**build_federation_token_payload())
    signin_token = fetch_aws_federation_signin_token(federation_token)
    return redirect(build_sign_in_url(signin_token),code='302')

@consolelogin_blueprint.route("/")
def index():
    profile_names = fetch_profile_names()
    return render_template('index.html', profile_names=profile_names)
