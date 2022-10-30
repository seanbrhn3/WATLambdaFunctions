from email.mime import image
import json
from sys import prefix
import boto3
import logging
import re
import base64

logging.basicConfig(level=logging.INFO)
S3 = boto3.client("s3")

# Invocation request type: X-Amz-Invocation-Type	method.request.header.InvocationType

def lambda_handler(event, context):
    try:
        # Predicted index of the shoe found in s3
        pred = shoe_recognition()
        shoe_name, shoe_image, links = locate_shoe(pred)
        shoe_info = {
            "name": shoe_name,
            "links": links,
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
    try:
        ENDPOINT_NAME = 'IC-data-1575382941' # Sagemaker endpoint
        runtime= boto3.client('runtime.sagemaker')
        # Downloading picture to upload to sagemaker nueral net
        with open("/tmp/postmantest4.jpg","wb") as data:
            S3.download_fileobj("visionprocessing", "postmantest4.jpg", data)

        with open("/tmp/postmantest4.jpg", 'rb') as f:
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
    except Exception as e:
        return f"{e}"
    
# Only searches for folders instead of content within them
def list_folders(s3_client, bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='', Delimiter='/')
    for content in response.get('CommonPrefixes', []):
        yield content.get('Prefix')
 
"""
    Notes:
        LOOK AT THIS FOR FILTERING: https://stackoverflow.com/questions/45601305/get-full-path-to-files-in-s3-using-boto3-nested-keys
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjectsV2
    
"""
def locate_shoe(pred):
    try:
        folders = list_folders(S3,"sagemakertestwat-dev")
        count = 0
        for folder in folders:
            if count == pred:
                object = S3.list_objects_v2(Bucket="sagemakertestwat-dev",Prefix=folder)
                image_name = object.get('Contents')[0].get("Key")
                image_string = download_image(image_name)
                # Image names look like this Adidas-Yeezy-Boost-350-Low-V2-Beluga/Adidas-Yeezy-Boost-350-Low-V2-Beluga0.jpg
                # So we need to remove everything from the '/' and after
                remove_point = image_name.index("/")
                image_name = image_name.replace(image_name[remove_point:],"")
                if "-" not in image_name:
                    image_name = image_name.replace(" ","-")
                links = generate_links(image_name)
                return image_name, image_string, links
            count +=1
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

def generate_links(name):
    stockx = f"https://stockx.com/{name}"
    goat = f"https://www.goat.com/sneakers/{name}"
    flight_club = f"https://www.flightclub.com/{name}"
    dtlr_men = f"https://www.dtlr.com/collections/men/products/{name}"
    dtlr_women = f"https://www.dtlr.com/collections/women/products/{name}"
    return [stockx,goat,flight_club,dtlr_men,dtlr_women]
