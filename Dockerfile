FROM python:2

WORKDIR /opt/sqldeveloperpassworddecryptor/
COPY requirements.txt sqldeveloperpassworddecryptor.py ./
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/python", "./sqldeveloperpassworddecryptor.py"]
