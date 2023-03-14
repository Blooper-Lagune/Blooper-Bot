FROM python:3.10-slim

WORKDIR /blooper

ADD . /blooper

RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python3", "blooper.py"]