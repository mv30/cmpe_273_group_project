import time
from sqs_utils import SQS_Utils
from configparser import ConfigParser
from execution_service import ExecutionService
from multiprocessing import Process

class ExecutorConsumer:
    
    worker_name: str
    queue_name: str

    def __init__(self, worker_name) -> None:
        self.worker_name = worker_name
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        self.queue_name = config_parser.get('AWS_RESOURCES','AWS_SQS_QUEUE_NAME')

    def start( self):
        sqs_utils = SQS_Utils(self.queue_name)
        while True:
            time.sleep(1)
            print(" {} : Polling for messages ".format(self.worker_name))
            messages = sqs_utils.receive_messages()
            for message in messages:
                print(" {} has message : {} ".format(self.worker_name, message))
                is_success = self.consume(message)
                if is_success:
                    sqs_utils.delete_messsage(message)

    def consume( self, message):
        execution_helper = ExecutionService()
        sqs_utils = SQS_Utils(self.queue_name)
        attributes, body = sqs_utils.unpack_message( message)
        token = attributes['token']
        print(" token:{} ".format(token))
        return execution_helper.process_token(token)


if __name__ == '__main__':
    consumers = [ ExecutorConsumer('Worker 1'), ExecutorConsumer('Worker 2') ]
    processes = []
    for i in range(len(consumers)):
        p = Process(target=consumers[i].start, args=())
        processes.append(p)
        p.start()
    for i in range(len(consumers)):
        processes[i].join()


