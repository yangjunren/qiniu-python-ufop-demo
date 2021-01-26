FROM python:3.6
ADD . /home/ubuntu/qiniu-python-ufop-demo
WORKDIR /home/ubuntu/qiniu-python-ufop-demo
RUN pip install -r requirements.txt
CMD python server.py