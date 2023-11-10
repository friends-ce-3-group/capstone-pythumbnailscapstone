# app.py
import os
import boto3
from PIL import Image

s3Bucket = os.environ['S3_BUCKET']
s3Key = os.environ['S3_KEY']
s3KeySplit = s3Key.split("/")
s3FileName = s3KeySplit[1]
tmpFilePath = '/tmp/'+s3FileName

print(f'This method converts an original image from {s3Bucket}/{s3Key} into a thumbnail.')

# connect to s3 resource
s3 = boto3.resource('s3', region_name='us-west-2')

# download the file from s3
s3.meta.client.download_file(s3Bucket, s3Key, tmpFilePath)
im = Image.open(tmpFilePath)
width, height = im.size
print(f'The image width is {width}')
print(f'The image height is {height}')

# resize
im.thumbnail((width/2, height/2))
im.save(tmpFilePath)
im = Image.open(tmpFilePath)
newWidth, newHeight = im.size
print(f'The new image width is {newWidth}')
print(f'The new image height is {newHeight}')

# upload the file to s3
s3.meta.client.upload_file(tmpFilePath, s3Bucket, 'thumbnails/'+s3FileName)