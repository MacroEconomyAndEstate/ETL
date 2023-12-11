import boto3
from botocore.exceptions import NoCredentialsError


class S3Uploader:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            self.s3.upload_file(file_name, self.bucket_name, object_name)
            return True
        except NoCredentialsError:
            # TODO: log
            return False
        except Exception as e:
            # TODO: log
            return False
