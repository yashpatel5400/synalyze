#!/bin/sh
# shell script for initializing Ubuntu AWS EC2 to run server

sudo apt-get update

sudo apt-get install -y gcc emacs24
sudo apt-get install -y python-dev python-virtualenv
sudo apt-get install -y python3-pip python3-dev

sudo apt-get install -y libffi-dev
sudo apt-get install -y portaudio19-dev
sudo apt-get install -y libssl-dev

sudo apt-get install -y mpg321
sudo apt-get install -y ffmpeg

git clone https://github.com/yashpatel5400/synalyze.git
cd synalyze
virtualenv synalyze
source synalyze/bin/activate
pip install -r requirements.txt
