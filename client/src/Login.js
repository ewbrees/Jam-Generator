import { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [userExists, setUserExists] = useState(false);


  const handleUsernameChange = (event) => {
    const value = event.target.value;
    if (value.length <= 20) { // Set the maximum character limit to 20 for the username
      setUsername(value);
    }
  };

  const handlePasswordChange = (event) => {
    const value = event.target.value;
    if (value.length <= 20) { // Set the maximum character limit to 50 for the password
      setPassword(value);
    }
  };
  const handleLoginButton = () => {
    // send login request to server with username and password
    // replace the URL with the endpoint for your server's login functionality
    fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/flask_login?username=${username}&password=${password}`, {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => {
        if (data !== "username or password incorrect") {
          setLoggedIn(true);
          console.log(loggedIn);
          // set session cookie with user session data
          document.cookie = `userSessionData=${JSON.stringify(data)}`;
        } else {
          setUserExists(false); // Reset userExists state to false if it was previously set to true during registration
          setLoggedIn(false);
          setPassword('');
          alert('Incorrect username or password'); // Inform the user that the username or password is incorrect
        }
      })
      .catch(error => {
        console.error('Error logging in:', error);
      });
  };
  
  const handleSubmit = (event) => {
    event.preventDefault();
    // send login request to server with username and password
    // replace the URL with the endpoint for your server's login functionality
    fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/flask_register?username=${username}&password=${password}`, {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => {
        // set user session data or redirect to home page based on response from server
        console.log(data);
        if (data !== "username already taken") {
          setLoggedIn(true);
          console.log(loggedIn);
          // set session cookie with user session data
          document.cookie = `userSessionData=${JSON.stringify(data)}`;
        } else {
          setUserExists(true);
        }
      })
      .catch(error => {
        console.error('Error logging in:', error);
      });
  };



  return (
    <div className="LoginContainer">
      <h1 className="LoginHeader">Create Account</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            <span className="InputText">Username</span>
            <input
              type="text"
              value={username}
              onChange={handleUsernameChange}
              className="InputL"
              maxLength={20}
              minLength={1} // Set the maximum character limit to 20 for the username
            />
          </label>
        </div>
        <div>
          <label>
            <span className="InputText">Password </span>
            <input
              type="password"
              value={password}
              onChange={handlePasswordChange}
              className="InputL"
              maxLength={20} // Set the maximum character limit to 50 for the password
              minLength={4}
            />
          </label>
        </div>
        <div>
        <button type="button" className="SubmitButtonL" onClick={handleLoginButton}>
          Login
        </button>
          <button type="submit" className="SubmitButtonL">Register</button>
        </div>
      </form>
      {userExists && (
        <p className = "ElseText">
          Username is already taken{' '}
          {/* <button className="SubmitButtonLog" onClick={() => handleLogin(false)}>login</button> instead of registering with these credentials? */}
        </p>
      )}
      {loggedIn && <Link to="/home" className="NowLogText">You are now logged in. Click here to go to the home page.</Link>}
    </div>
  );
}

export default LoginPage;
