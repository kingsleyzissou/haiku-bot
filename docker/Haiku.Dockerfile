FROM python:3

COPY src/haiku_detection.py /src/
COPY src/pre_processing.py /src/
COPY src/post_processing.py /src/
COPY src/twitter.py /src/
COPY src/test.py /src/
COPY .env ./

COPY requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /src/

CMD ["python3", "test.py"]