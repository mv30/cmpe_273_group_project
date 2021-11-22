from flask import Flask, request, jsonify
from s3utils import S3Utils
from execution_service import ExecutionEntity, ExecutionEntry, ExecutionService
from sqs_utils import SQS_Utils
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('config.ini')

AWS_SQS_QUEUE_NAME = config_parser.read('AWS_RESOURCES','AWS_SQS_QUEUE_NAME')

s3_helper = S3Utils()
sqs_helper = SQS_Utils()
execution_helper = ExecutionService()
app = Flask(__name__)

def handle_upload_source_code( token, file_ob):
    execution_helper.create_record(ExecutionEntry( None, token, None, 'INIT', []))
    s3_helper.upload_file_ob( file_ob, "{}/source_code.py".format(token))

def handle_add_dependencies( token, dependencies):
    execution_helper.update_record( ExecutionEntry( None, token, None, None, dependencies))

def handle_upload_input( token, file_ob):
    execution_helper.update_record( ExecutionEntry( None, token, True, None, None))
    s3_helper.upload_file_ob( file_ob, "{}/input.txt".format(token))

def handle_execute( token):
    message_attributes = {
        'token' : token
    }
    sqs_helper.send_message( AWS_SQS_QUEUE_NAME, message_attributes, None)
    execution_helper.update_record( ExecutionEntry( None, token, None, 'ENQUEUED', None))

@app.route('/hello')
def say_hello():
    return 'Hello'

@app.route('/upload-source-code/<token>', methods=['POST'])
def upload_source_code(token: str):
    handle_upload_source_code(token, request.stream)
    return 'Source Code Upload done'

@app.route('/add-dependecies/<token>', methods=['POST'])
def add_dependencies(token: str):
    handle_add_dependencies(token, request.get_json())
    return 'Dependecies added'

@app.route('/upload-input/<token>', methods=['POST'])
def upload_input(token: str):
    handle_upload_input(token, request.stream)
    return 'Input Upload done'

@app.route('/execute/<token>', methods=['POST'])
def run_source_code(token: str):
    handle_execute(token)
    return 'Submitted for execution'
