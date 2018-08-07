#!/bin/bash
#

# Start services
sudo service redis start
sudo service mongod start

# news pipeline
pushd ../src/news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &
popd

# recommendation service
pushd ../src/recommendation_service
python3 click_log_processor.py &
python3 recommendation_service.py &
popd

# news topic service
pushd ../src/news_topic_modeling_service/server
python3 server.py &
popd

# backend server
pushd ../src/backend_server
python3 service.py &
popd

# web server
pushd ../src/web/server
npm start &
popd

# list all processes
jobs -r
jobs -p

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
