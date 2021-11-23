import boto3
import json
from configparser import ConfigParser

class SQS_Utils:

    queue: None
    queue_name: None
    
    def __init__(self, queue_name) -> None:
        self.queue_name = queue_name
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        AWS_ACCESS_KEY_ID = config_parser.get('AWS_SECRETS', 'AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = config_parser.get('AWS_SECRETS', 'AWS_SECRET_ACCESS_KEY')
        AWS_REGION = config_parser.get('AWS_SECRETS', 'AWS_REGION')
        sqs = boto3.resource('sqs', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
        self.queue = sqs.get_queue_by_name(QueueName=self.queue_name)
    
    def pack_message( self, message_attributes, message_body):
        attributes = {}
        body = {}
        if message_attributes is not None:
            for (key, value) in message_attributes.items():
                attributes[key] = {
                    'StringValue': value,
                    'DataType': 'String'
                }
        if message_body is not None:
            body = message_body
        return ( attributes, body)

    def unpack_message( self, message):
        attributes = {}
        for (key,value) in message.message_attributes.items():
            attributes[key] = value['StringValue']
        body = json.loads(message.body)
        return  attributes, body

    def delete_messsage( self, messsage):
        messsage.delete()

    def send_message( self, message_attributes, message_body):
        attributes, body = self.pack_message( message_attributes, message_body)
        return self.queue.send_message(
            MessageBody=json.dumps(body),
            MessageAttributes=attributes
        )

    def receive_messages( self):
        messages = self.queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=7,
            WaitTimeSeconds=10)
        return messages


if __name__ == '__main__':
    
    sqs_helper = SQS_Utils('group_nine_executor_queue')

    # version1 

    # attributes = {
    #     'Name': 'Mayank',
    #     'University': 'SJSU'
    # }
    # body = {
    #     'data': [
    #         {
    #             'subject': 'CMPE-255',
    #             'name': 'Data Mining'
    #         },
    #         {
    #             'subject': 'CMPE-272',
    #             'name': 'Platforms'
    #         },
    #         {
    #             'subject': 'CMPE-273',
    #             'name': 'Distributed Systems'
    #         }
    #     ]
    # }
    # sqs_helper.send_message(attributes, body)

    # version 2

    # messages = sqs_helper.receive_messages()
    
    # for message in messages:
    #     attributes, body = sqs_helper.unpack_message(message)
    #     print(" message_attributes:{} message_body:{} ".format( attributes, body))
    #     sqs_helper.delete_messsage(message)
    
    # for message in messages:
    #     print(" message_id:{} message_attributes:{} message_body:{} ".format(message.message_id, message.message_attributes, message.body))

