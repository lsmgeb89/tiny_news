var bodyParser = require('body-parser');
var cors = require('cors');
var express = require('express');
var passport = require('passport');
var path = require('path');

// routers
var authRouter = require('./routes/auth');
var indexRouter = require('./routes/index');
var newsRouter = require('./routes/news');

var app = express();

// connect mongodb
var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

// use body-parser to convert user's post string to json
app.use(bodyParser.json());

// view engine setup
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');
app.use('/static',
        express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
app.use(cors());

// load passport strategies
app.use(passport.initialize());
var localSignUpStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignUpStrategy);
passport.use('local-login', localLoginStrategy);

const authChecker = require('./middleware/auth_checker');

// register rounters
app.use('/', indexRouter);
app.use('/auth', authRouter);
// authChecker must be put before newsRouter
// because we want to authenticate user before returning news
app.use('/news', authChecker);
app.use('/news', newsRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
