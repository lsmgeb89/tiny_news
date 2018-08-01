var jayson = require('jayson');

// create a client
var client = jayson.client.http({
  hostname: 'localhost',
  port: 4040
});

// test rpc method
function add(a, b, callback) {
  client.request('add', [a, b], function(err, response) {
    if (err) throw err;
    console.log(response);
    callback(response.result);
  });
}

function get_news_summaries_for_user(user_id, page_num, callback) {
  client.request('get_news_summaries_for_user', [user_id, page_num], function(err, response) {
    if (err) throw err;
    console.log(response);
    callback(response.result);
  });
}

module.exports = {
  add : add,
  get_news_summaries_for_user : get_news_summaries_for_user
};
