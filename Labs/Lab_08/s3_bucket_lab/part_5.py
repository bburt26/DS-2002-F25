import boto3
import requests

url = "https://upload.wikimedia.org/wikipedia/commons/b/b6/Mount_Everest_as_seen_from_Drukair2_PLW_edit_Cropped.jpg"
filename = "everest.jpg"

r = requests.get(url)
with open(filename, "wb") as f:
    f.write(r.content)

s3 = boto3.client('s3', region_name="us-east-1")
bucket = "ds2002-f25-jtg3ts"
key = filename

with open(filename, "rb") as data:
    s3.put_object(Body=data, Bucket=bucket, Key=key)

presigned = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': key},
    ExpiresIn=3600
)

