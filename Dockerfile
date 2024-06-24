FROM ubuntu:20.04

WORKDIR /

RUN apt-get update && apt-get install -y python3 python3-pip


RUN  DEBIAN_FRONTEND=noninteractive apt install -yq mysql-client pkg-config
RUN  DEBIAN_FRONTEND=noninteractive apt install -yq python3-dev default-libmysqlclient-dev build-essential

RUN python3 -m pip install mysqlclient
RUN python3 -m pip install mysql 

COPY . .

CMD ["/bin/bash"]
