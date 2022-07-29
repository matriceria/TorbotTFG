#!/bin/sh

apt-get install -y python3-socks
apt-get install -y python3-bs4
apt-get install -y python3-requests
apt-get install -y python3-termcolor
apt-get install -y wget
wget https://pypi.python.org/packages/7d/8e/83b6cec169e2af1ea82447af844012fa445a414bcba326342ed935274dcb/tldextract-2.2.0.tar.gz && \
tar xvf tldextract-2.2.0.tar.gz && \
cd tldextract-2.2.0 && \
python3 setup.py install
echo 'SOCKSPort 9050' >> /etc/tor/torrc
service tor start
