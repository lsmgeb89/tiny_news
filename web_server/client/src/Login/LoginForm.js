import React from 'react';
import './LoginForm.css';
import PropTypes from 'prop-types';

// es6: destructuring assignment
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment
const LoginForm = ({
  onSubmit,
  onChange,
  errors,
  user,
}) => (
  <div className="container">
    <div className="card-panel login-panel">
      <form className="col s12" action="/" onSubmit={onSubmit}>
        <h4 className="center-align">Login</h4>

        {errors.summary && <div className="row"><p className="error-message">{errors.summary}</p></div>}

        <div className="row">
          <div className="input-field col s12">
            <input className="validate" id="email" type="email" name="email" onChange={onChange}/>
            <label htmlFor='email'>Email</label>
          </div>
        </div>

        {errors.email && <div className="row"><p className="error-message">{errors.email}</p></div>}

        <div className="row">
          <div className="input-field col s12">
            <input className="validate" id="password" type="password" name="password" onChange={onChange}/>
            <label htmlFor='password'>Password</label>
          </div>
        </div>

        {errors.password && <div className="row"><p className="error-message">{errors.password}</p></div>}

        <div className="row right-align">
          <input type="submit" className="waves-effect waves-light btn indigo lighten-1" value='Log in'/>
        </div>
        <div className="row">
          <p className="right-align">New to Tiny News? <a href="/signup">Sign Up</a></p>
        </div>
      </form>
    </div>
  </div>
);

// static type check for parameters of arrow function
LoginForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  errors: PropTypes.object.isRequired,
  user: PropTypes.object.isRequired
}

export default LoginForm;
