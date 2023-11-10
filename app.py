# app.py
import os
import boto3

s3Bucket = os.environ['S3_BUCKET']
s3Key = os.environ['S3_KEY']
s3KeySplit = s3Key.split("/")
s3FileName = s3KeySplit[1]

print(f"Message":"This method converts an original image from {s3Bucket}/{s3Key} into a thumbnail.")

s3 = boto3.resource('s3', region_name='us-west-2')
origObject = s3.Object(bucket_name = s3Bucket, key = s3Key)

print(origObject.bucket_name)
print(origObject.key)
