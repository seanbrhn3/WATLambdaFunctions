import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    try:
        event = json.loads(event)
        client = boto3.client("s3")
        email = event["email"]
        now  = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        event["current_time"] = now
        with open(f"/tmp/{email}-{now}.json","w") as file:
            json.dump(event,file,indent=4)
            
        with open(f"/tmp/{email}-{now}.json","r",encoding='utf-8') as file:
            client.put_object(
                Body=json.dumps(file.readlines()),
                Bucket="wat-website-user-info",
                Key=f"{email}-{now}.json"
            )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "File Uploaded Successfully! Great Job!!!",
                }
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": f"{e}",
                }
            ),
        }

# event = {
#     "name":"sdfdsfsd",
#     "email":"testme@example.com",
#     "phone":"4443445553",
#     "message":"WAT IS AMAZING!!!"
# }
# ex = json.dumps(event)
# print(ex)
# print(lambda_handler(event,None))