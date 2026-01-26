import boto3
import os
from PIL import Image
from io import BytesIO
import json
client = boto3.client('s3')

def resize_image(src_bucket, src_key, des_bucket, des_key, max_size):
    """
    Resize image while maintaining aspect ratio.
    The longest edge will be resized to max_size, and the other edge will be scaled proportionally.
    
    Args:
        src_bucket: Source S3 bucket name
        src_key: Source object key
        des_bucket: Destination S3 bucket name
        des_key: Destination object key
        max_size: Maximum size for the longest edge (int)
    """
    in_mem_file = BytesIO()
    
    # Get the image from S3
    file_byte_string = client.get_object(Bucket=src_bucket, Key=src_key)['Body'].read()
    im = Image.open(BytesIO(file_byte_string))
    
    # Get original dimensions
    original_width, original_height = im.size
    print(f'Original size: {original_width}x{original_height}')
    
    # Calculate new dimensions maintaining aspect ratio
    # thumbnail() resizes based on the longest edge while maintaining aspect ratio
    im.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    
    # Get new dimensions after resize
    new_width, new_height = im.size
    print(f'Resized to: {new_width}x{new_height} (max edge: {max_size})')
    
    # Save the resized image
    im.save(in_mem_file, format=im.format)
    in_mem_file.seek(0)
        
    # save to new folder in S3.
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

    # Define maximum sizes for the longest edge
    max_size_1000 = 1000
    max_size_500 = 500
    max_size_200 = 200
    max_size_100 = 100
    
    client = boto3.client('s3')
    for obj in event['Records']:
        bucket_name = obj['s3']['bucket']['name']
        object_key = obj['s3']['object']['key']
        
        print(f'Resizing file: {bucket_name}/{object_key}')
        
        # Resize to different sizes while maintaining aspect ratio
        resize_image(bucket_name, object_key, bucket_name, 'resized_1000/' + object_key, max_size_1000)
        resize_image(bucket_name, object_key, bucket_name, 'resized_500/' + object_key, max_size_500)
        resize_image(bucket_name, object_key, bucket_name, 'resized_200/' + object_key, max_size_200)
        resize_image(bucket_name, object_key, bucket_name, 'resized_100/' + object_key, max_size_100)
    
        print('Resize completed!')

    return {
        'statusCode': 200,
        'body': json.dumps('Process completed!')
    }