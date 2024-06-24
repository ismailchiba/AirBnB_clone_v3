FROM python:3.4
MAINTAINER Nteboheleng Lioja <ntebohelengd@gmail.com>

RUN git clone https://github.com/Vriendelik/AirBnB_clone_v3.git
WORKDIR /root/AirBnB
RUN pip3 install virtualenv
RUN pip install -r requirements.txt
