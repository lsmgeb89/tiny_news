# Tiny News: Real Time News Scraping and Recommendation System

## Summary

* Built a single-page web application for users to browse personalized real-time news ([React][react], [Node.js][node.js], [SOA][soa], [RPC][rpc])
* Implemented industry standard user authentication and authorization by hashing salted passwords and using JSON Web Token ([JWT][jwt])
* Implemented a data pipeline which monitors, scrapes, deduplicates and stores latest news ([MongoDB][mongodb], [Redis][redis], [RabbitMQ][rabbitmq], [TF-IDF][tf-idf])
* Implemented a news recommendation service by applying time decay preference model on collected users' click activities
* Designed and built an offline training pipeline for news topic modeling by 2-layer [convolutional neural networks][cnn] ([Tensorflow][tensorflow])
* Deployed an online news topic classification service by using the trained model

[react]: https://reactjs.org/
[node.js]: https://nodejs.org/en/
[soa]: https://en.wikipedia.org/wiki/Service-oriented_architecture
[rpc]: https://en.wikipedia.org/wiki/Remote_procedure_call
[jwt]: https://en.wikipedia.org/wiki/JSON_Web_Token
[mongodb]: https://www.mongodb.com/
[redis]: https://redis.io/
[rabbitmq]: https://www.rabbitmq.com/
[tf-idf]: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
[cnn]: https://en.wikipedia.org/wiki/Convolutional_neural_network
[tensorflow]: https://www.tensorflow.org/

## Design

### Modules

1. Web Client and Server
    * user sign up
    * user login
    * load news
2. Backend Server
3. News Pipeline
    * monitor news
    * scrape news
    * dedupe news with similar topic
4. Recommendation Service
    * recommendate personalized news based on logs of click event
5. News Topic Classification
    * create offline modeling of news topic classification
    * provide online service of news topic classification

### Server List

1. Web Server
    * type: HTTP Server
    * tcp port: `3000`
    * APIs:
      * `/`
      * `/signup`
      * `/login`
      * `/userId/<user_id>/pageNum/<page_num>`
      * `/userId/<user_id>/newsId/<news_id>`
2. Backend Server
    * type: RPC Server
    * tcp port: `4040`
    * APIs:
      * `get_news_summaries_for_user(user_id, page_num)`
      * `log_news_click_for_user(user_id, news_id)`
3. Recommendation Server
    * type: RPC Server
    * tcp port: `5050`
    * API:
      * `get_preference_for_user(user_id)`
4. Classification Server
    * type: RPC server
    * tcp port: `6060`
    * API:
      * `classify(news_text)`
5. Redis Server:
    * tcp port: `6379`
    * key-value pairs:
      * `<news_digest, True>` for precise news deduplication, expiring in one day
      * `<user_id, recent 200 news digest>` for caching this user's recent 200 news
6. MongoDB Server
    * tcp port: `27017`
    * database: `tiny-news`
    * collections:
      * `news` stores `<news_digest, news json object>`
      * `users` stores doc that contains attributes `email` and `password`
      * `user_preference_model` stores doc that contains `userId` and `preference`
7. RabbitMQ‎
    * queues
      * `scrape-queue` stores tasks (news json object) for scraper to download news text
      * `dedupe-queue` stores news json object for similar topic deduplication
      * `log-clicks-queue` stores json object that contains which user clicks which news at which timestamp

### News Pipeline

![news_pipeline]

### Click Event Log Processing and Recommendation Pipeline

![click_log]

[news_pipeline]: doc/news_pipeline.svg "News Pipeline"
[click_log]: doc/click_log_recommendation.svg "Click Event Log Processing and Recommendation Pipeline"
