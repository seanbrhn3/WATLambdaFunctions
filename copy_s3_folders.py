import boto3
import logging
import os
logging.basicConfig(level=logging.INFO)
client = boto3.client("s3")
def copy_btw_s3_buckets():
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
    
def copy_kaggle_data():
    subfolders = [ f.path for f in os.scandir("/Users/seanbrown/Downloads/sneaker_dataset/images/train") if f.is_dir() ]
    print(subfolders)
    
copy_kaggle_data()