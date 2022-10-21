import json
from unittest.mock import call

import pytest
import pprint
import requests

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "test": "body"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }
    
def test_response():
    
    return {
    "message": "{\"Messages\": [{\"MessageId\": \"ed6fb5e4-6702-4f6d-b159-a799d1593f9f\", \"ReceiptHandle\": \"AQEBukt12Irwp10VyWAGXIpLPR+GwQr52qOcDZCB3G5yvkWeBVcrBEuZ3fIIU7y0qmU/ECUgaWU4ncdDbxfXPy4Z5oHpWLkmqhySsJEoZhbYUa667MtnRQmVS4gDCjppo0LVD4oqixcjatx1p2PNJxVmzRGXw89xW3ozhUsyluNEVdhJyNpG7tzpONpc6yHX2RUjajFkaolgxfx/hzrpYchC5wSnE+kHGZTItjOa9xA4ZPA9HZxFnha3HWxgf2Pzd7X6oHS9ypHNI3DWEoZZz8rfeo978ELmvhxPAGilqaX3GBloUqTqfmcBmOA8j+cmbdMQPqGvdyBTPcvC9YP5FgvLealz+SRMOn9qmOufNZsfdvh+8qn0BGOd0p4Rtn4laXw9unNFsG0nmQkHpCNh+7McJQ==\", \"MD5OfBody\": \"12c88f89867ed25c17beed6df3415ef3\", \"Body\": \"{\\\"version\\\":\\\"1.0\\\",\\\"timestamp\\\":\\\"2022-09-27T05:04:41.462Z\\\",\\\"requestContext\\\":{\\\"requestId\\\":\\\"249dd116-76e1-49cd-88da-8a1b370fb78e\\\",\\\"functionArn\\\":\\\"arn:aws:lambda:us-east-1:814180570813:function:sage-make-upload-image-SageMakerImageUploadFunctio-fMHEwryeJo2v:$LATEST\\\",\\\"condition\\\":\\\"Success\\\",\\\"approximateInvokeCount\\\":1},\\\"requestPayload\\\":{},\\\"responseContext\\\":{\\\"statusCode\\\":200,\\\"executedVersion\\\":\\\"$LATEST\\\"},\\\"responsePayload\\\":{\\\"statusCode\\\": 200, \\\"headers\\\": {\\\"Content-Type\\\": \\\"*/*\\\", \\\"Access-Control-Allow-Origin\\\": \\\"*\\\"}, \\\"body\\\": \\\"Your shoe is: \\\\\\\"adidas Yeezy Boost  OG Light Brown\\\\\\\"\\\", \\\"isBase64Encoded\\\": false}}\"}], \"ResponseMetadata\": {\"RequestId\": \"655d1d4b-4d01-564f-ad93-46e6884f769c\", \"HTTPStatusCode\": 200, \"HTTPHeaders\": {\"x-amzn-requestid\": \"655d1d4b-4d01-564f-ad93-46e6884f769c\", \"date\": \"Wed, 28 Sep 2022 03:44:14 GMT\", \"content-type\": \"text/xml\", \"content-length\": \"1726\"}, \"RetryAttempts\": 0}}"
}

def test_lambda_handler(apigw_event, mocker):
    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"

def call_async():
    res = requests.get("https://bp5h50tym0.execute-api.us-east-1.amazonaws.com/Prod/async")
    return res.json

pprint.pprint(call_async())