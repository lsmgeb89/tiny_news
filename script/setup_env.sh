#!/bin/bash
#

# install Node.js
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install npm --global

# install js packages for web client
pushd ../src/web/client
npm install
popd

# install js packages for web server
pushd ../src/web/server
npm install
popd

# install python packages
sudo apt install -y python3-pip
sudo -H pip3 install --upgrade pip
pip3 install --user -r ../src/requirements.txt

# install MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# install Redis
sudo apt install -y redis-server

# build model
pushd ../src/news_topic_modeling_service/trainer
mkdir -p ../model
python3 news_class_trainer.py
popd

# build web client
pushd ../src/web/client
npm run build
popd
