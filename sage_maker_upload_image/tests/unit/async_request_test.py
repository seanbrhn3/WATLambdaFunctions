import asyncio
import aiohttp
import json
import os
import base64
import re
import requests

def request_sage():
    headers = {
        "content-type": "application/json",
        "InvocationType": "Event"
    }
    test = requests.get("https://zdnlp0vdld.execute-api.us-east-1.amazonaws.com/Prod/sage",headers=headers)
    print(test.json())
    
    
def request_async_reciever():
    headers = {
        "content-type": "application/json",
    }
    test_async = requests.get("https://bp5h50tym0.execute-api.us-east-1.amazonaws.com/Prod/async",headers=headers)
    print(test_async.json())

async def test_api_gateweay():
    #Tells api gatway that this will be an async call https://aws.plainenglish.io/executing-a-long-running-aws-lambda-function-with-api-gateway-as-a-trigger-cd000ddaef26
    headers = {
        "content-type": "application/json",
        "InvocationType": "Event"
               }
    test = requests.get("https://zdnlp0vdld.execute-api.us-east-1.amazonaws.com/Prod/sage",headers=headers)
    
    #json parameter automatically sets the content header. So don't add header arguments (https://docs.aiohttp.org/en/stable/client_advanced.html)
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zdnlp0vdld.execute-api.us-east-1.amazonaws.com/Prod/sage",headers=headers) as response:
            print(f"response status: {response.status}")
            shoe = await response.json()
            print(f"The shoe is: {shoe}")
            
def decode_image(image):
    image = open(image, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read)
    return image_64_encode
    
def test_body():
        image = decode_image("testpicture12.jpg").decode("utf-8")
        image = image.replace("\\","")
        return {
        "body": image
    }
        
def write_to_File():
    body ={
        "body": '{ "test": "body"}'
    }

    image = decode_image("testpicture12.jpg").decode("utf-8")
    image = image.strip("\n")
    image = image.replace('\\',"backSlask")
    image_reged = re.sub(r'\\',"Replaced",image)
    body["body"] = image_reged
    with open("test.json","w") as file:
        json.dump(body,file)
            
def main():
    request_sage()
main()