import time
from sqs_utils import SQS_Utils
from configparser import ConfigParser
from execution_service import ExecutionService
import concurrent.futures

class ExecutorConsumer:
    
    worker_name: str
    queue_name: str
    sqs_utils: SQS_Utils
    execution_helper: ExecutionService

    def __init__(self, worker_name) -> None:
        self.worker_name = worker_name
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        self.queue_name = config_parser.get('AWS_RESOURCES','AWS_SQS_QUEUE_NAME')
        self.sqs_utils = SQS_Utils( self.queue_name)
        self.execution_helper = ExecutionService()

    def start( self, worker_name):
        while True:
            time.sleep(1)
            print(" {}: Polling for messages ".format(self.worker_name))
            messages = self.sqs_utils.receive_messages()
            for message in messages:
                print(" {} has message : {} ".format(self.worker_name, message))
                is_success = self.consume(message)
                if is_success:
                    self.sqs_utils.delete_messsage(message)

    def consume( self, message):
        attributes, body = self.sqs_utils.unpack_message( message)
        token = attributes['token']
        print(" token:{} ".format(token))
        return self.execution_helper.process_token(token)


if __name__ == '__main__':
    executor = ExecutorConsumer('worker')
    executor.start('Worker')
    # consumers = [ ExecutorConsumer('Worker 1'), ExecutorConsumer('Worker 2') ]
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    # executor.submit( consumers[0].start, 'Worker 1')
    # executor.submit( consumers[1].start, 'Worker 2')
    # # executor.map(consumers[0].start)
    # # executor.map(consumers[1].start)


