import React, { useState, useEffect } from 'react';
import './HomePage.css';
import Navbar from './Navbar';

  const handleClick = () => {
    // add window here
    //useEffect(() => {
      const cookieData = document.cookie
        .split(';')
        .find(cookie => cookie.startsWith('userSessionData='));
  
      if (cookieData) {
        const userData = JSON.parse(cookieData.split('=')[1]);
        const loginWindow = window.open(`https://jam-gen-backend-t6vk3.ondigitalocean.app/login?token=${userData}`, 'loginWindow', 'width=400,height=400');
       /* loginWindow.fetch(`https://rgkeeney-refactored-xylophone-x4g997r5j9vfrv5-5000.preview.app.github.dev/flask_login?username=${username}&password=${password}`, {
          method: 'GET',
        })*/
        const receiveMessage = (event) => {
          if (event.origin === 'https://jam-gen-backend-t6vk3.ondigitalocean.app/callback') {
            if (event.data === 'success') {
              loginWindow.close();
            }
          }
        };
      }
     // const loginWindow = window.open('https://www.sjbaker.org/humor/cardboard_dog.html', 'width=400,height=400');
        /*const receiveMessage = (event) => {
          if (event.origin === 'https://rgkeeney-refactored-xylophone-x4g997r5j9vfrv5-5000.preview.app.github.dev/callback') {
            if (event.data === 'success') {
              loginWindow.close();
            }
          }
        };*/
    //}, []);
    //window.location.href = 'https://jam-gen-backend-t6vk3.ondigitalocean.app/login';
  };

function HomePage() {
    return (
        <div>
          <Navbar />
          <div className="Home-header">
            <header className="Title">
              <p> JAM GENERATOR </p>
            </header>
            <header className="Sub_Title">
              <p> Generate a Spotify playlist tailored for you in seconds </p>
            </header>
          </div>
          <div className="Bottom">
              
              {/* 
                <Link to="/quiz-page">
                  <button className="QuizButton">What's Your Type?</button>
                </Link>
              */}
              
              <button className="SpotButton" onClick={handleClick}>
                Login to Spotify To Save Playlists
              </button>
          </div>
        </div>
    );
};


export default HomePage;