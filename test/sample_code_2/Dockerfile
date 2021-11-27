FROM python:3

WORKDIR /app/

COPY . .

RUN pip install "flask"

RUN pip install "pymongo"

RUN pip install "pymongo[srv]"

CMD [ "python3","app.py"]