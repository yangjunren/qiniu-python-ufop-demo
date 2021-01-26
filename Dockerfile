FROM python:3.6
ONBUILD ADD . /usr/src/qiniu-python-ufop-demo
ONBUILD RUN /usr/local/bin/python-build --dir /usr/src/qiniu-python-ufop-demo
ONBUILD RUN pip install -r requirements.txt
CMD python server.py