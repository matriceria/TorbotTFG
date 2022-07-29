FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

# install tor
RUN add-apt-repository "deb http://deb.torproject.org/torproject.org xenial main"
# RUN add-apt-repository "deb-src http://deb.torproject.org/torproject.org xenial main"
RUN gpg --keyserver keys.gnupg.net --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 && \
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -
RUN apt-get update
RUN apt-get install -y tor deb.torproject.org-keyring


# Copy torbot

RUN mkdir -p /usr/app/src
COPY TorBoT/ /usr/app/src
COPY install-script.sh /usr/app/src
WORKDIR /usr/app/src

# install python packages
# RUN sh install-script.sh
RUN pip install -r requirements.txt
