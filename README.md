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
