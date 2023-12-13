import boto3
from botocore.exceptions import NoCredentialsError


class S3Uploader:
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key)

    def put_object(self, file_name, csv_buffer):
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=csv_buffer.getvalue())
            print(f"Object {file_name} uploaded successfully.")
            return True
        except NoCredentialsError:
            print("No AWS credentials found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
