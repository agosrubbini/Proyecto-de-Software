from flask import current_app as app

def get_bucket_and_server_minio():

    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']

    return minio_client, bucket_name