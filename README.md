# Clean empty dirs in minio
### This repo need to build image for recursively cleanup empty dirs.

In `clean-empty-dirs-s3.py` use [boto3](https://github.com/boto/boto3) plugin whitch install with `whl` files located in `boto3` dir.

Script `clean-empty-dirs-s3.py` need global envs for start:
- ACCESS_KEY - secret accsesskey for access in s3 
- SECRET_KEY - secret key for access in s3 
- BUCKET_NAME - name of bucket wich need to cleanup
- S3_ENDPOINT_URL - url of api for s3

#### Examplle of local run 
```bash
python -m pip install boto3

export ACCESS_KEY="1231233123" \
export SECRET_KEY="321321231" \
export BUCKET_NAME="my-backup-name" \
export S3_ENDPOINT_URL="https://s3-api.local" \
python ./clean-empty-dirs-s3.py
```
