import io
import os

import boto3
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Create a session using your credentials
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

# Create an S3 client
s3 = session.client('s3')


class S3Operations():
    def _init_(self):
        pass

    def get_all_bucket_names(self) -> list[str]:
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        return bucket_names

    def get_all_objects(self, bucket_name=AWS_BUCKET_NAME) -> list[str]:
        response = s3.list_objects_v2(Bucket=bucket_name)
        object_keys = [obj['Key'] for obj in response.get('Contents', [])]
        return object_keys

    def get_object(self, object_key: str, bucket_name=AWS_BUCKET_NAME) -> dict:
        try:
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            return response
        except s3.exceptions.NoSuchKey:
            raise ValueError(
                f"Object with key '{object_key}' not found in bucket '{bucket_name}'")
        except Exception as e:
            raise RuntimeError(f"Error retrieving object from S3: {str(e)}")

    def upload_object(self, object_key: str, file_path: str, bucket_name=AWS_BUCKET_NAME) -> None:
        # Convert to absolute path if it's not already
        abs_file_path = os.path.abspath(file_path)

        # Check if file exists
        if not os.path.exists(abs_file_path):
            raise FileNotFoundError(
                f"The file {abs_file_path} does not exist.")

        try:
            s3.upload_file(abs_file_path, bucket_name, object_key)
            print(
                f"Successfully uploaded {abs_file_path} to {bucket_name}/{object_key}")
        except Exception as e:
            raise RuntimeError(f"Error uploading file to S3: {str(e)}")

    def download_object(self, object_key: str, bucket_name=AWS_BUCKET_NAME) -> bytes:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read()

    def delete_object(self, object_key: str, bucket_name=AWS_BUCKET_NAME) -> dict:
        response = s3.delete_object(Bucket=bucket_name, Key=object_key)
        return response

    def delete_bucket(self, bucket_name=AWS_BUCKET_NAME) -> dict:
        response = s3.delete_bucket(Bucket=bucket_name)
        return response

    def create_bucket(self, bucket_name=AWS_BUCKET_NAME) -> dict:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                    'LocationConstraint': AWS_REGION_NAME})
        return response

    def copy_object(self, source_bucket_name: str, source_object_key: str, destination_bucket_name: str, destination_object_key: str) -> dict:
        copy_source = {'Bucket': source_bucket_name, 'Key': source_object_key}
        response = s3.copy_object(
            Bucket=destination_bucket_name, CopySource=copy_source, Key=destination_object_key)
        return response

    def move_object(self, source_bucket_name: str, source_object_key: str, destination_bucket_name: str, destination_object_key: str) -> dict:
        self.copy_object(source_bucket_name, source_object_key,
                         destination_bucket_name, destination_object_key)
        response = self.delete_object(source_object_key, source_bucket_name)
        return response


my_s3 = S3Operations()

# try:
#     my_s3.upload_object(
#         object_key='itachi',
#         file_path='itachi.png',  # or provide the full path here
#         bucket_name='gen-ai-hacks'
#     )
# except FileNotFoundError as e:
#     print(f"File not found: {e}")
# except RuntimeError as e:
#     print(f"An error occurred during upload: {e}")

try:
    file = my_s3.get_all_objects('gen-ai-hacks')
    print(f"got the file: {file}")

#     # image_data = file['Body'].read()

# # Open the image using Pillow (PIL)
#     image = Image.open(io.BytesIO(image_data))

# # Display the image
#     image.show()

# # Optionally, save it to a file
#     image.save("output_image.jpg")
except ValueError as e:
    print(f"Object not found: {e}")
except RuntimeError as e:
    print(f"An error occurred during retrieval: {e}")
