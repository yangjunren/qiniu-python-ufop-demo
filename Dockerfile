FROM python:3.6
ADD . /usr/src/qiniu-python-ufop-demo
WORKDIR /usr/src/qiniu-python-ufop-demo
RUN pip install -r requirements.txt
CMD python server.py