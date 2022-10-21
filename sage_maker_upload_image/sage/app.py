import json
import boto3
import logging
import re
import base64

logging.basicConfig(level=logging.INFO)
S3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        # Predicted value of the shoe found in s3
        pred = shoe_recognition()
        shoe_name, shoe_image = locate_shoe(pred)
        shoe_info = {
            "name": shoe_name,
            "image": shoe_image
        }
        respone_body = {
            "statusCode":200,
            "headers":{
                "Content-Type": "*/*",
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(shoe_info),
            "isBase64Encoded": True
        }
        return respone_body
    except Exception as e:
        logging.error(f"[!]Unable  to  invoke endpoint, error: {e}")
        respone_body = {
        "statusCode":500,
        "headers":{
            "Content-Type":"application/json",
            "X-Amzn-ErrorType":"InvalidParameterException",
            'Access-Control-Allow-Origin': '*'
        },
        "body": f"error: {e}",
        "isBase64Encoded":False
        }
        return respone_body
    
    
 # This will return the page # in S3 where you can locate the shoe   
def shoe_recognition():
        ENDPOINT_NAME = 'IC-data-1575382941' # Sagemaker endpoint
        runtime= boto3.client('runtime.sagemaker')
        # Downloading picture to upload to sagemaker nueral net
        with open("/tmp/postmantest3.jpg","wb") as data:
            S3.download_fileobj("visionprocessing", "postmantest3.jpg", data)

        with open("/tmp/postmantest3.jpg", 'rb') as f:
            payload = f.read()
            payload = bytearray(payload)
        # Run image through nueral net to get the best result
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                        ContentType='application/x-image',
                                        Body=payload)
        
        #  Response is a byte array so you must decode.
        result = json.loads(response['Body'].read().decode())

        pred = result.index(max(result))
        return pred
 
 # Finds the shoe based on the index given from shoe recognitions
"""
 ex:
        index = 50
        max # of items per page = 1000
        index/ max = 5 - page # to lookat
        remainder = 0 index of that shoe at page 5
        
    1. Use NextToken to skip pages
    2. Prefix all dir with '/'
    
    Notes:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjectsV2
    
"""
def locate_shoe(pred):
    # Set paginator to the max length of 1000
    paginator = S3.get_paginator('list_objects_v2')
    maxItems = 1000
    pageSize = 1000
    paginator_config = {
        "MaxItems":maxItems,
        "Pagesize":pageSize,
    }
    
    # Page to look at
    page = maxItems/pred
    page = int(page)
    logging.info(f"[+] Looking at page {page}")
    
    # The Remainder is the exact position of the shoe
    index = maxItems%pred
    logging.info(f"[+] Locating shoe at position: {index}")
    # Formating shoe names to remove .jpg and remvove duplicates
    count = 0
    logging.info("[+] Collecting Shoe names...")
    try:
        # Grab all the names of shoes in the S3 bucket
        shoe_folders = paginator.paginate(Bucket="sagemakertestwat-dev",PaginationConfig=paginator_config)
        next_page = None
        while count < page+1:
            for shoes_pagination in shoe_folders:
                # Flip through each page to youo find the one the shoe is located in
                if count == page:
                    logging.info(f"[+] Collecting shoes on page {page}, looking for shoe at position {index}")
                    position = index/len(shoes_pagination.get("Contents"))
                    #  Now that you've found the shoes page return the position in on the page.
                    image_name = shoes_pagination.get("Contents")[int(position)].get("Key")
                    image_string = download_image(image_name)
                    return image_name, image_string
                # If shoe_folder returns a string its the starting token of the next position
                if 'NextContinuationToken' in shoes_pagination.keys():
                    next_page = shoes_pagination.get('NextContinuationToken')
                    break
                
            paginator_config = {
                "MaxItems":maxItems,
                "Pagesize":pageSize,
                'StartingToken':next_page
            }
            shoe_folders = paginator.paginate(Bucket="sagemakertestwat-dev",PaginationConfig=paginator_config)
            count += 1
    except Exception as e:    
        return f"[!] Unable to retrieve shoe, error: {e}"
            
    return "Unable to locate shoe"
    
#  Get image from s3 then converts it to base64 string
def download_image(image_name):
    try:
        revised_image_name = image_name.replace("/","")
        logging.info(f"[+] Writing image to /tmp/{image_name}")
        with open(f"/tmp/{revised_image_name}","wb") as data:
            S3.download_fileobj("sagemakertestwat-dev", image_name, data)
            
        logging.info("[+] Reading image to base64 encoding")
        image = open(f"/tmp/{revised_image_name}", 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        return image_64_encode.decode('utf-8') # Decode image to a string to dump it to json
    except Exception as e:
        logging.error(f"[!] error loading image {e}")

print(lambda_handler(None,None))