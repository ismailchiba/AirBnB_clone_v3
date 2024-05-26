FROM python:3.4
MAINTAINER SimonUwezo <simonnmwangi@gmai.com>

RUN git clone https://github.com/glyif/AirBnB_clone_v3.git ~/AirBnB
WORKDIR /root/AirBnB
RUN pip3 install virtualenv
RUN pip install -r requirements.txti
