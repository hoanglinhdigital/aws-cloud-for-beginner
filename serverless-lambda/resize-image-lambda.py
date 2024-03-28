import boto3
import os
from PIL import Image
import pathlib
from io import BytesIO
import json
client = boto3.client('s3')

def resize_image (src_bucket, src_key, des_bucket, des_key, size):
    in_mem_file = BytesIO()
    
    file_byte_string = client.get_object(Bucket=src_bucket, Key=src_key)['Body'].read()
    im = Image.open(BytesIO(file_byte_string))
    resized_image = im.resize(size)

    resized_image.save(in_mem_file, format=im.format)
    in_mem_file.seek(0)
        
    # save to new folder
    response = client.put_object(
    Body=in_mem_file,
    Bucket=des_bucket,
    Key=des_key
    )
        
def lambda_handler(event, context):
    #For debug only
    print('bucket name is:\n')
    print(event['Records'][0]['s3']['bucket']['name'])
    print('object key is:\n')
    print(event['Records'][0]['s3']['object']['key'])

    size1000 = 1000, 1000
    size500 = 500, 500
    size200 = 200, 200
    size100 = 100, 100
    
    in_mem_file = BytesIO()
    client = boto3.client('s3')
    
    bucket_name = ''
    object_key = ''
    for obj in event['Records']:
        bucket_name = obj['s3']['bucket']['name']
        object_key = obj['s3']['object']['key']
        
        print('resize file: ' + bucket_name + '/' + object_key)
        
        resize_image(bucket_name, object_key, bucket_name, 'resized_1000/' + object_key, size1000)
        resize_image(bucket_name, object_key, bucket_name, 'resized_500/' + object_key, size500)
        resize_image(bucket_name, object_key, bucket_name, 'resized_200/' + object_key, size200)
        resize_image(bucket_name, object_key, bucket_name, 'resized_100/' + object_key, size100)
    
        print('resize completed!')

    return {
        'statusCode': 200,
        'body': json.dumps('Process completed!')
    }