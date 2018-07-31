var cors = require('cors');
var express = require('express');
var path = require('path');

var indexRouter = require('./routes/index');
var newsRouter = require('./routes/news');

var app = express();

// connect mongodb
var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

// view engine setup
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');
app.use('/static',
        express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
app.use(cors());

// register rounters
app.use('/', indexRouter);
app.use('/news', newsRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
