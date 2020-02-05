import boto3
import os
import sys
import configparser
from botocore.exceptions import ClientError
import argparse

access_key = ""
secret = ""
bucket = ""
region = ""
localfile = "test.txt"


def get_settings():
    try:
        pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
        config = configparser.ConfigParser()
        config.read(pathname + "/settings.cfg")
        global access_key
        global secret
        global bucket
        global region
        access_key = config["default"]["access_key"]
        secret = config["default"]["secret"]
        bucket = config["default"]["bucket"]
        region = config["default"]["region"]
    except Exception:
        print("Unable to load values from the config file. Check the file exists in the same directory as the script and it has the right format and values")
        exit(10)


def upload_to_aws(local_file, remote_file):
    response = []
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      config=boto3.session.Config(signature_version='s3v4'),
                      region_name=region,
                      aws_secret_access_key=secret)

    print("Will upload " + local_file + " to " + bucket + "/"+remote_file)
    try:
        s3.upload_file(local_file, bucket, remote_file)
        print("Upload Successful")
    except Exception as error:
        print("Could not upload local file to s3")
        print(error)
        exit(-1)
    try:

        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': remote_file}, ExpiresIn=(60*60*24*1)))
        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': remote_file},
                                                  ExpiresIn=(60 * 60 * 24 * 2)))
        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': remote_file},
                                                  ExpiresIn=(60 * 60 * 24 * 3)))
        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': remote_file},
                                                  ExpiresIn=(60 * 60 * 24 * 4)))
        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': remote_file},
                                                  ExpiresIn=(60 * 60 * 24 * 5)))
        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': remote_file},
                                                  ExpiresIn=(60 * 60 * 24 * 6)))
        response.append(s3.generate_presigned_url('get_object', Params={'Bucket': bucket,'Key': remote_file}, ExpiresIn=604800))
    except ClientError as e:
        logging.error(e)
        return None
    return response


def get_file_path():
    parser = argparse.ArgumentParser(description="Select a file to upload to S3")
    parser.add_argument(
        "--file",
        "-f",
        #default='default',
        help="Specifies the file to be uploaded ",
        required=True
    )
    args = parser.parse_args()
    file = args.file

    args = parser.parse_args()
    if os.path.isfile(file):
        return file
    else:
        pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
        file = pathname + "/" + file
        return file




# uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')

get_settings()
file = get_file_path()
remote_file = os.path.basename(file)
urls = upload_to_aws(file,remote_file)
count = 1
for x in urls:
    print(str(count) + " days to expire " + x)
    count+=1
