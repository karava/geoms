# storages.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import logging
import boto3

class PublicMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_PUBLIC_STORAGE_BUCKET_NAME
    custom_domain = f"{bucket_name}.s3.amazonaws.com"
    file_overwrite = False
    location = settings.FOLDER_NAME

    def delete(self, name):
        name = self._normalize_name(self._clean_name(name))
        self.bucket.Object(name).delete()
        return super().delete(name)

    def list_all_filenames(self):
        """
        List all file names in the storage.
        """
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        paginator = s3_client.get_paginator('list_objects_v2')

        file_names = []
        for page in paginator.paginate(Bucket=self.bucket_name):
            if "Contents" in page:
                for obj in page['Contents']:
                    file_names.append(obj['Key'])

        return file_names

class PrivateMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_PRIVATE_STORAGE_BUCKET_NAME
    custom_domain = f"{bucket_name}.s3.amazonaws.com"
    default_acl = 'private'
    file_overwrite = False
    querystring_auth = True
    location = settings.FOLDER_NAME