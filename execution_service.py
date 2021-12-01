from flask.globals import session
from sqlalchemy import Column, Integer, String, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configparser import ConfigParser

from sqlalchemy.sql.operators import op
from docker_utils import Docker_Utils

from s3utils import S3Utils
import os

Base = declarative_base()

class ExecutionEntity(Base):
    
    __tablename__ = 'execution_detail'
    id =Column( Integer, primary_key=True)
    token = Column( String, unique=True)
    input_provided = Column( Boolean, default=False)
    status = Column( String, nullable=False)
    dependencies = Column( JSON, nullable=True)

    def __repr__(self) -> str:
        return "Excution id:{} \n token:{} \n status:{} \n dependencies:{}  "\
            .format( self.id, self.token, self.status, self.dependencies)

    def get_entry( self):
        return ExecutionEntry( id=self.id, token=self.token,  input_provided=self.input_provided, status=self.status, dependencies=self.dependencies)

class ExecutionEntry:

    id : int
    token: str
    input_provided: bool
    status: str
    dependencies: list

    def __init__( self, id, token, input_provided, status, dependencies) -> None:
        self.id = id
        self.token = token
        self.input_provided = input_provided
        self.status = status
        self.dependencies= dependencies

    def get_entity(self):
        execution_entity = ExecutionEntity()
        execution_entity.id = self.id
        execution_entity.token = self.token
        execution_entity.input_provided = self.input_provided
        execution_entity.status = self.status
        execution_entity.dependencies = self.dependencies
        return execution_entity

class ExecutionService:

    engine: None
    Session: None
    s3_helper: S3Utils
    docker_helper: Docker_Utils

    def __init__(self) -> None:
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        POSTGRES_CONNECTION_STRING = config_parser.get('POSTGRES','POSTGRES_CONNECTION_STRING')
        self.engine = create_engine(POSTGRES_CONNECTION_STRING)
        self.Session = sessionmaker(bind=self.engine)
        self.s3_helper = S3Utils()
        self.docker_helper = Docker_Utils()

    def create_record( self, entry: ExecutionEntry) -> ExecutionEntry:
        entity = entry.get_entity()
        session = self.Session()
        session.add(entity)
        session.commit()
        entry_created = entity.get_entry()
        session.close()
        return entry_created

    def find_by_token( self, token_arg) -> ExecutionEntry:
        entry = None
        session = self.Session()
        entity = session.query(ExecutionEntity).filter_by(token=token_arg).first()
        if entity is not None:
            entry = entity.get_entry()
        session.close()
        return entry
    
    def update_record( self, entry: ExecutionEntry) -> ExecutionEntry:
        session = self.Session()
        entity : ExecutionEntity = session.query(ExecutionEntity).filter_by(token=entry.token).first()
        if entry.input_provided is not None:
            entity.input_provided = entry.input_provided
        if entry.status is not None:
            entity.status = entry.status
        if entry.dependencies is not None:
            entity.dependencies = entry.dependencies
        session.commit()
        entry = entity.get_entry()
        session.close()
        return entry

    def process_token( self, token):
        entry = self.find_by_token(token)

        try:

            cwd = os.getcwd()
            os.mkdir("{}/var/{}".format( cwd, token))

            SOURCE_CODE_FILE_PATH = "./var/{}/source_code.py".format(token)
            INPUT_FILE_PATH = "./var/{}/input.txt".format(token)
            OUTPUT_FILE_PATH = "./var/{}/output.txt".format(token)
            DOCKER_FILE_PATH = "./var/{}/Dockerfile".format(token)
            DOCKER_BUILD_COMMAND = " docker build -t {} ./var/{} ".format(token, token)
            DOCKER_RUN_COMMAND = " docker run --rm -i {} {} > {} "
            INPUT_COMMAND_COMPONENT = ''

            with open( SOURCE_CODE_FILE_PATH, 'wb') as source_code_file:
                self.s3_helper.download_file_ob( source_code_file, "{}/source_code.py".format(token))
            if entry.input_provided:
                INPUT_COMMAND_COMPONENT = " < {} ".format(INPUT_FILE_PATH)
                with open( INPUT_FILE_PATH, 'wb') as input_file:
                    self.s3_helper.download_file_ob( input_file, "{}/input.txt".format(token))
            with open( DOCKER_FILE_PATH, 'w') as docker_file:
                self.docker_helper.gen_file( docker_file, entry.dependencies)
            
            DOCKER_RUN_COMMAND = DOCKER_RUN_COMMAND.format(token, INPUT_COMMAND_COMPONENT, OUTPUT_FILE_PATH)
            
            # execute command
            os.system(DOCKER_BUILD_COMMAND)
            os.system(DOCKER_RUN_COMMAND)

            with open(OUTPUT_FILE_PATH, 'rb') as output_file:
                self.s3_helper.upload_file_ob(output_file, "{}/output.txt".format(token))
            self.update_record(ExecutionEntry( id=None, token=token, input_provided=None, status='SUCCESS', dependencies=None))
            return True
        
        except:
            self.update_record(ExecutionEntry( id=None, token=token, input_provided=None, status='FAILED', result=None))
            return False



if __name__ == '__main__':

    execution_service = ExecutionService()
    res = ExecutionEntry(None, None, None, None, None)

    # version_1
    # entry = ExecutionEntry( id=None, token='_a_sda_s__qw__wq', status='ENQUEUED', result=None)
    # res = execution_service.create_record(entry)

    # version_2
    # res = execution_service.find_by_token('_a_sda_s__qw__wq')

    # version_3
    # entry = ExecutionEntry( id=None, token='_a_sda_s__qw__wq', input_provided=None,status='COMPLETED', dependencies=[])
    # res = execution_service.create_record(entry)
    # res = execution_service.update_record(entry)
    # res = execution_service.find_by_token('_a_sda_s__qw__wq')

    # version_4
    execution_service.process_token('zzsxa213987asda')

    print(type(res))
    print(res.get_entity())

