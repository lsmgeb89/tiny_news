const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;

module.exports = new PassportLocalStrategy(
  {
    usernameField: 'email',
    passwordField: 'password',
    passReqToCallback: true
  },
  (req, email, password, done) => {
    const userData = {
      email: email.trim(),
      password: password
    };

    console.log('local signup strategy: ', userData);

    // create a new user directly into mongodb without checking duplicate
    // because mongodb will check for us and throw error if duplicate
    const newUser = new User(userData);

    newUser.save((err) => {
      console.log('Save new user!');

      if (err) {
        return done(err);
      }

      return done(null);
    });
  }
);
