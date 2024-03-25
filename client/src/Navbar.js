import React, { useEffect, useState } from 'react';
import './Navbar.css';
import { Link, useLocation, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [displayName, setDisplayName] = useState('');
  const [loggedIn, setLoggedIn] = useState(false); // Add loggedIn state

  useEffect(() => {
    const cookieData = document.cookie
      .split(';')
      .find(cookie => cookie.startsWith('userSessionData='));

    if (cookieData) {
      const userData = JSON.parse(cookieData.split('=')[1]);
      fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/token_to_username?token=${userData}`)
        .then(response => response.json())
        .then(data => {
          setDisplayName(data);
          setLoggedIn(true); // Set loggedIn to true when user data is retrieved
        });
    }
  }, []);

  const handleLogout = () => {
    // Delete the cookie and set loggedIn to false
    document.cookie = 'userSessionData=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    setLoggedIn(false);
    navigate('/home');
  };

  let linkTo, linkText, linkTo2, linkText2, showLogout;

  switch (location.pathname) {
    case '/output-page':
      linkTo = '/home';
      linkText = 'Home';
      linkTo2 = '/quiz-page';
      linkText2 = 'Generate New';
      showLogout = true; // Show Logout on /output-page
      break;
    case '/quiz-page':
      linkTo = '/home';
      linkText = 'Home';
      linkTo2 = '/output-page';
      linkText2 = 'Search Playlists';
      showLogout = false; // Hide Logout on /quiz-page
      break;
    case '/home':
      linkTo = '/quiz-page';
      linkText = 'Generate New';
      linkTo2 = '/output-page';
      linkText2 = 'Search Playlists';
      showLogout = false; // Hide Logout on /home
      break;
    default:
      break;
  }

  return (
    <header className="TopNav">
      <nav>
        <ul className="NavLeft">
          <li>
            <Link to={linkTo}>{linkText}</Link>
          </li>
        </ul>
        <ul className="NavMidLeft">
          {loggedIn && (
            <p className="NavLink"> 
              Welcome, {displayName}!
            </p>
          )}
        </ul>
        <ul className="NavMidRight">
          {loggedIn ? (
            <li>
              <button className="NavButton" onClick={handleLogout}>
                Logout
              </button>
            </li>
          ) : (
            <li>
              <Link to="/" className="NavLinkCen">
                Login
              </Link>
            </li>
          )}
        </ul>
        <ul className="NavRight">
          <li>
            <Link to={linkTo2} className="NavLink">
              {linkText2}
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Navbar;
