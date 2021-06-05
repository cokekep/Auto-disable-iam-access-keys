import os
import boto3
from botocore.exceptions import ClientError
import datetime
import json

# Get RETENTION and Key Status from environment variable
DAYS_RETENTION = os.getenv('DAYS_RETENTION', 180)
STATUS_FILTER = os.getenv('STATUS_FILTER', 'Active')

iam_client = boto3.client('iam')


def list_access_key(user, days_filter, status_filter):
    keydetails = iam_client.list_access_keys(UserName=user)
    key_details = {}
    user_iam_details = []

    # Some user may have 2 access keys.
    for keys in keydetails['AccessKeyMetadata']:
        if (days := time_diff(keys['CreateDate'])) >= days_filter and keys['Status'] == status_filter:
            key_details['UserName'] = keys['UserName']
            key_details['AccessKeyId'] = keys['AccessKeyId']
            key_details['days'] = days
            key_details['status'] = keys['Status']
            user_iam_details.append(key_details)
            key_details = {}

    return user_iam_details


def time_diff(keycreatedtime):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now-keycreatedtime
    return diff.days


def create_key(username):
    access_key_metadata = iam_client.create_access_key(UserName=username)
    access_key = access_key_metadata['AccessKey']['AccessKeyId']
    secret_key = access_key_metadata['AccessKey']['SecretAccessKey']


def disable_key(access_key, username):
    try:
        iam_client.update_access_key(
            UserName=username, AccessKeyId=access_key, Status="Inactive")
        print(access_key + " has been disabled.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)


def delete_key(access_key, username):
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print(access_key + " has been deleted.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)


def lambda_handler(event, context):
    details = iam_client.list_users(MaxItems=300)
    users = details['Users']
    for user in users:
        print("UserName :", user.get('UserName'))
        userName = user.get('UserName')
        user_iam_details = list_access_key(
            user=userName, days_filter=DAYS_RETENTION, status_filter=STATUS_FILTER)
        print("Number of old Access Keys :", len(user_iam_details))
        for _ in user_iam_details:
            disable_key(access_key=_['AccessKeyId'], username=_['UserName'])
            delete_key(access_key=_['AccessKeyId'], username=_['UserName'])
            # create_key(username=_['UserName'])
            print("Old Access Key Id :", _['AccessKeyId'])

    return {
        'statusCode': 200,
    }