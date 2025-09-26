import os
import subprocess
import logging
import sys
import boto3

dbt_config_vars = {
    "s3_bucket_target": "s3://vigia-data-lake-dl-artifacts-bucket-dev-a14b31"
    ,"iam_role":""
    ,"glue_db":""
}

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Logger initialized")

s3 = boto3.client("s3")

bucket = "vigia-data-lake-dl-artifacts-bucket-dev-a14b31"
prefix = "poc_transformations_dbt/"
local_dir = "/tmp/project"

os.makedirs(local_dir, exist_ok=True)

def download_prefix(bucket, prefix, local_dir):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/"):  # skip folders
                continue
            local_path = os.path.join(local_dir, key.replace(prefix, "", 1))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(bucket, key, local_path)

download_prefix(bucket, prefix, local_dir)
logger.info(">>> Download complete.")

logger.info(f"Dir: {os.listdir('/tmp/project')}")
# Run dbt
logger.info("running dbt")
result_with_output= subprocess.run(
    ["dbt", "run", "--profiles-dir", f"{local_dir}/profiles", "--project-dir", local_dir, "--debug"],
    check=True
)
logger.info(result_with_output.stdout)