
class Docker_Utils:

    def gen_file( self, file, dependencies):
        file.write('FROM python:3 \n\n')
        file.write('WORKDIR /app/ \n\n')
        file.write('COPY . . \n\n')
        for dependency in dependencies:
            file.write('RUN pip install "{}"\n\n'.format(dependency))
        file.write('CMD [ "python3","source_code.py"]')
        file.close()
