import json
import boto3
import logging

def lambda_handler(event, context):
    ENDPOINT_NAME = 'IC-data-1575382941' # Sagemaker endpoint
    runtime= boto3.client('runtime.sagemaker')
    s3 = boto3.client("s3")
    
    # Grab all the names of shoes in the s3 bucket
    shoe_folders = s3.list_objects_v2(Bucket="sagemakertestwat-dev")
    shoes = []
    for shoe in shoe_folders.get("Contents"):
        print(shoe.get("Key",None))
        shoes.append(shoe.get("Key",None))
        
    with open("/tmp/testpicture12.jpg","wb") as data:
        s3.download_fileobj("visionprocessing", "testpicture12.jpg", data)

    with open("/tmp/testpicture12.jpg", 'rb') as f:
        payload = f.read()
        payload = bytearray(payload)
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/x-image',
                                       Body=payload)

    result = json.loads(response['Body'].read().decode())

    pred = result.index(max(result))
    print(f"[+] Check this prediction: {pred}, class: {shoes[pred]}")
    
    respone_body = {
        "statusCode":200,
        "headers":{
            "info":"image"
        },
        "body": json.dumps(shoes[pred]),
        "isBase64Encoded":True

    }
    return respone_body

print(lambda_handler(None,None))