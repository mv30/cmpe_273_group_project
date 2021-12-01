import boto3
from configparser import ConfigParser

class S3Utils:

    s3: None
    bucket_name: None

    def __init__(self) -> None:
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        AWS_ACCESS_KEY_ID = config_parser.get('AWS_SECRETS', 'AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = config_parser.get('AWS_SECRETS', 'AWS_SECRET_ACCESS_KEY')
        AWS_REGION = config_parser.get('AWS_SECRETS', 'AWS_REGION')
        AWS_S3_BUCKET_BUCKET_NAME = config_parser.get('AWS_RESOURCES', 'AWS_S3_BUCKET_BUCKET_NAME')
        self.bucket_name = AWS_S3_BUCKET_BUCKET_NAME
        self.s3 = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

    def upload_file_ob( self, read_file_ob, storage_path):
        return self.s3.upload_fileobj( read_file_ob, self.bucket_name, storage_path)

    def download_file_ob( self, write_file_ob, storage_path):
        return self.s3.download_fileobj( self.bucket_name, storage_path, write_file_ob)
    
    def get_presigned_url( self, token):
        return self.s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'execution-files',
                                                            'Key': "{}/output.txt".format(token)},
                                                    ExpiresIn=600)

    
if __name__ == '__main__':
    s3utils = S3Utils()
    url = s3utils.get_presigned_url('as01ass8123asd')
    print(url)
    with open('/Users/mayankverma/CMPE-273/cmpe_273_group_project/test/sample_file.txt','rb') as file_ob:
        s3utils.upload_file_ob( file_ob, 'trials/sample.text')
    with open('./test/downloaded_test.txt','wb') as download_file:
        s3utils.download_file_ob( download_file, 'trials/sample.text')
    