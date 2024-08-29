import os
import sys
import boto3

required_env_vars = ['ACCESS_KEY', 'SECRET_KEY', 'BUCKET_NAME', 'S3_ENDPOINT_URL']

missing_vars = [var for var in required_env_vars if os.getenv(var) is None]

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
bucket_name = os.getenv('BUCKET_NAME')
endpoint_url = os.getenv('S3_ENDPOINT_URL')

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=endpoint_url
)

def is_empty_directory(bucket, prefix):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    
    if 'CommonPrefixes' in response and len(response['CommonPrefixes']) > 0:
        return False
    
    if 'Contents' in response and len(response['Contents']) > 0:
        return False

    return True

def delete_empty_directories(bucket, prefix=''):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    
    if 'CommonPrefixes' in response:
        for common_prefix in response['CommonPrefixes']:
            sub_prefix = common_prefix['Prefix']
            delete_empty_directories(bucket, sub_prefix)
    
    if is_empty_directory(bucket, prefix):
        print(f"Deleting empty directory: {prefix}")
        delete_all_versions(bucket, prefix)

def delete_all_versions(bucket, prefix=''):
    paginator = s3.get_paginator('list_object_versions')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        versions = page.get('Versions', []) + page.get('DeleteMarkers', [])
        for version in versions:
            s3.delete_object(
                Bucket=bucket,
                Key=version['Key'],
                VersionId=version['VersionId']
            )
            print(f"Deleted {version['Key']} with version {version['VersionId']}")

delete_empty_directories(bucket_name)
