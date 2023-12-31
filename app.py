# app.py
import os
import boto3
import uuid
from dotenv import load_dotenv
from PIL import Image, ImageOps
from mysql import connector


load_dotenv()
s3Bucket = os.environ['S3_BUCKET']
s3Key = os.environ['S3_KEY']
s3KeySplit = s3Key.split("/")
s3FolderName = s3KeySplit[0]
s3FileName = s3KeySplit[1]
tmpFilePath = '/tmp/'+s3FileName

if s3FolderName != 'originals':
    print(f'Ignore Event as object is not created in the originals folder.')
    exit()

print(f'This method converts an original image from {s3Bucket}/{s3Key} into a thumbnail.')

# connect to s3 resource
s3 = boto3.resource('s3', region_name='us-west-2')

# download the file from s3
s3.meta.client.download_file(s3Bucket, s3Key, tmpFilePath)
im = Image.open(tmpFilePath)
width, height = im.size
print(f'The initial image width is {width} and height is {height}')

# resize for original
size = (500, 700)
ImageOps.fit(im, size).save(tmpFilePath)
im = Image.open(tmpFilePath)
newWidth, newHeight = im.size
print(f'The new original image width is {newWidth} and height is {newHeight}')
# upload the original to s3 (overwrite existing original image)
s3.meta.client.upload_file(tmpFilePath, s3Bucket, 'resized/'+s3FileName)

# resize for thumbnail
size = (180, 252)
ImageOps.fit(im, size).save(tmpFilePath)
im = Image.open(tmpFilePath)
newWidth, newHeight = im.size
print(f'The new thumbnail image width is {newWidth} and height is {newHeight}')
# upload the thumbnail to s3
s3.meta.client.upload_file(tmpFilePath, s3Bucket, 'thumbnails/'+s3FileName)


# insert an entry into CardsCatalog DB
s3FileNameParts = s3FileName.split('-')
accessType = s3FileNameParts[0]
category = s3FileNameParts[1]

mydb = None
try: 
    mydb = connector.connect(
    host=os.getenv('ENDPOINT_PROXY'),
    user=os.getenv('DBUSER'),
    password=os.getenv('DBPASS'),
    database=os.getenv('DBNAME')
    )
except:
    mydb = connector.connect(
    host=os.getenv('ENDPOINT'),
    user=os.getenv('DBUSER'),
    password=os.getenv('DBPASS'),
    database=os.getenv('DBNAME')
    )

query = """INSERT INTO CardsCatalog (cardKey, category, path, backgroundColor) VALUES ('{}', '{}', '{}', '{}')""".format(str(uuid.uuid4()), category, s3FileName, '#ffffff')
print(query)
try:
    with mydb.cursor() as cursor:
        cursor.execute(query)
        mydb.commit()
        print('Image inserted into CardsCatalog table successfully')

        query = "SELECT * FROM {}".format('CardsCatalog')
        cursor.execute(query)
        result = cursor.fetchall()
        print('select all result:', result)

except Exception as err:
    data = { "Error": str(err) }
    print(data)

