var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();

/* GET news list. */
// url: localhost:3000/news/userId/1@1.com/pageNum/2
// :userId and :pageNum is placeholder to extract value from url
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
  console.log('Fetching news...');
  user_id = req.params['userId'];
  page_num = req.params['pageNum'];

  rpc_client.get_news_summaries_for_user(user_id, page_num, function(response) {
    res.json(response);
  });
});

module.exports = router;
