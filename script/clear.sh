#!/bin/bash
#

# clear Redis
redis-cli flushall

# clear MongoDB
mongo tiny-news --eval "db.dropDatabase()"
mongo user --eval "db.dropDatabase()"

# clear RabbitMQ‎
pushd ../src/news_pipeline
python3 queue_helper.py
popd

# clear model
pushd ../src/news_topic_modeling_service/
rm -rf model
popd

# clear js packages for web client
pushd ../src/web/client
rm -rf node_modules
rm -rf build
popd

# clear js packages for web server
pushd ../src/web/server
rm -rf node_modules
popd
