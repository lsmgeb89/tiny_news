class Auth {
  // when a user logins in or registers successfully,
  // server sends token and client just stores it.
  static authenticateUser(token, email) {
    localStorage.setItem('token', token);
    localStorage.setItem('email', email);
  }

  static isUserAuthenticated() {
    return localStorage.getItem('token') != null;
  }

  // when a user logins out, client just clears token.
  static deauthenticateUser() {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
  }

  // send token along with get more news request
  static getToken() {
    return localStorage.getItem('token');
  }

  // show user name on page
  static getEmail() {
    return localStorage.getItem('email');
  }
}

export default Auth;
