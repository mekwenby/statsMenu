FROM python:3.10.4
COPY . /App
WORKDIR /App
RUN pip3 install -r requirements.txt -i "http://mirrors.aliyun.com/pypi/simple" --trusted-host "mirrors.aliyun.com"
EXPOSE 12380
CMD uwsgi --ini uwsgi.ini