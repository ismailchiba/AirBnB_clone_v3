FROM python:3.4
MAINTAINER YourName <danniwide.1981@gmail.com>

RUN git clone https://github.com/danniwide1234/AirBnB_clone_v3.git ~/AirBnB
WORKDIR /root/AirBnB
RUN pip3 install virtualenv
RUN pip3 install -r requirements.txt

