FROM python:3

COPY . .

COPY requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /src/

CMD ["python", "ye.py"]