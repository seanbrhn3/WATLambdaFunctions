from curses import start_color
import json
import boto3
# SQS Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message
# URL = os.environ["SQS_URL"] # Add this as an envrionment variables
SQS = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        queue = check_queue("https://sqs.us-east-1.amazonaws.com/814180570813/PredictedShoe")
        respone_body = {
            "statusCode":200,
            "headers":{
                "Content-Type": "application/json",
            },
            "body": queue,
            "isBase64Encoded": False
        }
        return respone_body
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "body": f"No data in queue: {e}",
                }
            ),
        }

def check_queue(url):
    try:
        # Checks SQS queue for any shoe predictions from the sagemaker_lambda function
        response  = SQS.receive_message(QueueUrl=url,MaxNumberOfMessages=1)
        for res in response.get("Messages"):
            resp= res.get("Body")
            resp = json.loads(resp)
            body = resp.get('responsePayload').get("body")
            if 'image' in body and 'name' in body:
                return body
            
        return  "No messages in queue"
    except Exception as e:
        return f"[!] error retrieving message {e}"

def generate_links(name):
    stockx = f"https://stockx.com/{name}"
    goat = f"https://www.goat.com/sneakers/{name}"
    flight_club = f"https://www.flightclub.com/{name}"
    dtlr_men = f"https://www.dtlr.com/collections/men/products/{name}"
    dtlr_women = f"https://www.dtlr.com/collections/women/products/{name}"
    return [stockx,goat,flight_club,dtlr_men,dtlr_women] 