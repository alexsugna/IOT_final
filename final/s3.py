import boto3
import config

def upload(filename):
    """
    Upload filename to the S3 bucket.
    """
    try:
        bucket = boto3.client('s3', aws_access_key_id=config.s3_access_key,
                                    aws_secret_access_key=config.s3_secret_key)
        bucket.upload_file(filename, config.bucket_name, filename)
        print("{} uploaded to S3 bucket successfully.".format(filename))
        return True
    except FileNotFoundError:
        print("{} not found.".format(filename))
        return False

def delete(filename):
    """
    Delete a file from the s3 bucket.
    """
    try:
        bucket = boto3.client('s3', aws_access_key_id=config.s3_access_key,
                                    aws_secret_access_key=config.s3_secret_key)
        bucket.delete_object(Bucket=config.bucket_name, Key=filename)
        print("{} successfully deleted.".format(filename))
        return True
    except:
        print("file not deleted. Make sure you have the correct path.")
        return False
