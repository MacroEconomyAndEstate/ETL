import requests
import pandas as pd
from domain.real_estate.real_estate_data_processor import RealEstateDataProcessor
from s3.s3_uploader import S3Uploader
from io import StringIO
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    env_path = os.path.join(os.path.dirname(__file__), 'resources', 'secret.env')
    load_dotenv(env_path)

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = os.getenv('AWS_BUCKET_NAME')
    s3_uploader = S3Uploader(aws_bucket_name, aws_access_key_id, aws_secret_access_key)

    p = RealEstateDataProcessor()

    df = p.get_monthly_real_estate_df()
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_uploader.put_object("monthly_real_estate.csv", csv_buffer)
    csv_buffer.seek(0)
    csv_buffer.truncate(0)

    df = p.get_leading_50_df()
    df.to_csv(csv_buffer, index=False)
    s3_uploader.put_object("leading_50.csv", csv_buffer)
    csv_buffer.seek(0)
    csv_buffer.truncate(0)

    df = p.get_pir_df()
    df.to_csv(csv_buffer, index=False)
    s3_uploader.put_object("pir.csv", csv_buffer)
    csv_buffer.seek(0)
    csv_buffer.truncate(0)

    df = p.get_quarterly_real_estate_df()
    df.to_csv(csv_buffer, index=False)
    s3_uploader.put_object("quarterly_real_estate.csv", csv_buffer)
    csv_buffer.seek(0)
    csv_buffer.truncate(0)
