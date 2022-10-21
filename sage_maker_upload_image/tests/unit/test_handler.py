import json
import sys
import pytest
import base64
import sage
from sage.app import lambda_handler


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "test": "body"}'
    }


def test_lambda_handler(apigw_event):
    apigw_event["body"] = decode_image("testpicture12.jpg")
    ret = lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 200
    assert "Your shoe is:" in ret["body"]
    
def test_lambda_handler_failure(apigw_event):
    # Using weird byte test
    apigw_event["body"] = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00'b'\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
    ret = lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 500
    assert "error:" in ret["body"]
    
def decode_image(image):
    image = open(image, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read).decode("utf-8")
    return image_64_encode
