var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
  // index.html is in ../../client/build
  // return app (index.html) created by react to users
  // node.js server to server that app
  res.sendFile("index.html",
               { root: path.join(__dirname, '../../client/build')});
});

module.exports = router;
