FROM python:3.7

ADD sns_project/requirements/webapp.txt /data/webapp.txt

RUN pip install --upgrade pip
RUN pip install gunicorn

RUN pip install -r /data/webapp.txt

RUN mkdir /app

WORKDIR /app

#CMD [ "bash"]