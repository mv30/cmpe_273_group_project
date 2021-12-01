import time
from sqs_utils import SQS_Utils
from configparser import ConfigParser
from execution_service import ExecutionService

class ExecutorConsumer:
    
    queue_name: str
    sqs_utils: SQS_Utils
    execution_helper: ExecutionService

    def __init__(self) -> None:
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        self.queue_name = config_parser.read('AWS_RESOURCES','AWS_SQS_QUEUE_NAME')
        self.sqs_utils = SQS_Utils( self.queue_name)
        self.execution_helper = ExecutionService()

    def start( self):
        while True:
            time.sleep(2)
            print(' Polling for messages')
            messages = self.sqs_utils.receive_messages( self.queue_name)
            for message in messages:
                is_success = self.consume(message)
                if is_success:
                    self.sqs_utils.delete_messsage(message)

    def consume( self, message):
        attributes, body = self.sqs_utils.unpack_message( message)
        token = attributes['token']
        return self.execution_helper.process_token(token)


