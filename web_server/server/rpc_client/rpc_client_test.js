var client = require('./rpc_client');

// invoke 'add'
client.add(1, 2, function(response) {
  console.assert(response == 3);
});

// invoke 'get_news_summaries_for_user'
client.get_news_summaries_for_user('test_user', 1, function(response) {
  console.assert(response != null);
});
