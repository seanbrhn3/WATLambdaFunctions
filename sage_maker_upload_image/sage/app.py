import json
from winreg import ExpandEnvironmentStrings
import boto3
import logging
import re
logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    ENDPOINT_NAME = 'IC-data-1575382941' # Sagemaker endpoint
    runtime= boto3.client('runtime.sagemaker')
    s3 = boto3.client("s3")
    paginator = s3.get_paginator('list_objects_v2')
    # Grab all the names of shoes in the s3 bucket
    shoe_folders = paginator.paginate(Bucket="sagemakertestwat-dev")
    shoes = set()
    logging.info("[+] Collecting Shoe names...")
    try:
        for shoes_pagination in shoe_folders:
            for shoe in shoes_pagination.get("Contents"):
                shoe_info = shoe.get("Key",None)
                # Filter on [ints,/, .jpg]
                shoe_info_fixed = re.sub(".jpg","",shoe_info)
                shoe_info_fixed1 = re.sub("/","",shoe_info_fixed)
                shoe_info_fixed2 = re.sub("\d+","",shoe_info_fixed1)
                shoes.add(shoe_info_fixed2)
                
        shoes = list(shoes)
    except Exception as e:
        logging.error(f"[!] {e}: Could not retrieve all shoes")
        
    logging.info(f"[+] {len(shoes)} collected.")
    
    # Downloading picture to upload to sagemaker nueral net
    try:
        with open("/tmp/testpicture12.jpg","wb") as data:
            s3.download_fileobj("visionprocessing", "testpicture12.jpg", data)

        with open("/tmp/testpicture12.jpg", 'rb') as f:
            payload = f.read()
            payload = bytearray(payload)
    except Exception as e:
        logging.error(f"[!] Error downloading and writing to image: {e}")
        
    # Run image through nueral net to get the best result
    try:
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                        ContentType='application/x-image',
                                        Body=payload)
        
        #  Response is a byte array so you must decode.
        result = json.loads(response['Body'].read().decode())

        pred = result.index(max(result))
        logging.info(f"[+] Check this prediction: {pred}, class: {shoes[pred]}")
    except Exception as e:
        logging.error(f"[!] Unable  to  invoke endpoint {e}")
    
    respone_body = {
        "statusCode":200,
        "headers":{
            "info":"image"
        },
        "body": json.dumps(shoes[pred]),
        "isBase64Encoded":True

    }
    return respone_body
