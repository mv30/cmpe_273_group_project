from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from s3utils import S3Utils
from execution_service import ExecutionEntity, ExecutionEntry, ExecutionService
from sqs_utils import SQS_Utils
from configparser import ConfigParser
import json

config_parser = ConfigParser()
config_parser.read('config.ini')
AWS_SQS_QUEUE_NAME = config_parser.get('AWS_RESOURCES','AWS_SQS_QUEUE_NAME')

s3_helper = S3Utils()
sqs_helper = SQS_Utils(AWS_SQS_QUEUE_NAME)
execution_helper = ExecutionService()
app = Flask(__name__)
CORS(app, support_credentials=True)

@cross_origin(supports_credentials=True)
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
    sqs_helper.send_message( message_attributes, None)
    execution_helper.update_record( ExecutionEntry( None, token, None, 'ENQUEUED', None))

def handle_poll( token):
    res = {}
    entry = execution_helper.find_by_token(token)
    res['status'] = entry.status
    if entry.status == 'SUCCESS':
        res['url'] = s3_helper.get_presigned_url(token)
    return res

@app.route('/hello')
@cross_origin(supports_credentials=True)
def say_hello():
    return 'Hello'

@app.route('/upload-source-code/<token>', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_source_code(token: str):
    handle_upload_source_code(token, request.stream)
    return 'Source Code Upload done'

@app.route('/add-dependecies/<token>', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_dependencies(token: str):
    handle_add_dependencies(token, request.get_json())
    return 'Dependecies added'

@app.route('/upload-input/<token>', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_input(token: str):
    handle_upload_input(token, request.stream)
    return 'Input Upload done'

@app.route('/execute/<token>', methods=['POST'])
@cross_origin(supports_credentials=True)
def run_source_code(token: str):
    handle_execute(token)
    return 'Submitted for execution'

@app.route('/poll/<token>', methods=['GET'])
@cross_origin(supports_credentials=True)
def poll_status(token):
    return jsonify(handle_poll(token))
