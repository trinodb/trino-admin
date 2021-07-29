FROM ubuntu:18.04

COPY . /src

WORKDIR /src

RUN \
  apt-get update && \
  apt-get install -y python python-pip && \
  pip install -r requirements.txt && \
  make dist-offline && \
  tar -xzf dist/trino-admin*.tar.gz -C /opt && \
  cd /opt/trino-admin && \
  ./install-trinoadmin.sh && \
  cd / && \
  rm -rf /src && \
  apt-get clean 

WORKDIR /
