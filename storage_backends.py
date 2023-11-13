# storages.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import logging

class PublicMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_PUBLIC_STORAGE_BUCKET_NAME
    custom_domain = f"{bucket_name}.s3.amazonaws.com"
    file_overwrite = False
    location = settings.FOLDER_NAME

    def _save(self, name, content):
        logger = logging.getLogger('django.storages')
        logger.info(f"Saving file to S3: {name}")
        return super()._save(name, content)

    def delete(self, name):
        logger = logging.getLogger('django.storages')
        logger.info(f"Deleting file from S3: {name}")
        return super().delete(name)

class PrivateMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_PRIVATE_STORAGE_BUCKET_NAME
    custom_domain = f"{bucket_name}.s3.amazonaws.com"
    default_acl = 'private'
    file_overwrite = False
    querystring_auth = True
    location = settings.FOLDER_NAME