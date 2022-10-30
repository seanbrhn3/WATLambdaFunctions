import boto3
import logging
logging.basicConfig(level=logging.INFO)
client = boto3.client("s3")
paginator = client.get_paginator('list_objects_v2')
bucket = "sagemakertestwat-dev"
paginator = client.get_paginator('list_objects_v2')
maxItems = 150000
pageSize = 10000
paginator_config = {
    "MaxItems":maxItems,
    "Pagesize":pageSize,
}
shoe_folders = paginator.paginate(Bucket=bucket,PaginationConfig=paginator_config)
count = 0
for index in shoe_folders:
    content = index.get("Contents")
    for i in content:
        key = i.get("Key")
        client.copy_object(Bucket="sagemakertestwat",CopySource=f"/{bucket}/{key}",Key="data/folder-"+key)
        logging.info(f"[+] Copying {key}")
logging.info(f"[+] Complete.")