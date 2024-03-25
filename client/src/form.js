import React, { useEffect, useState } from 'react';
import './form.css'

function PlaylistForm() {
  const [genre, setGenre] = useState('');
  const [playlistname, setPlaylistName] = useState('');
  const [popularity, setPopularity] = useState(50);
  const [mood, setMood] = useState('');
  const [numSongs, setNumSongs] = useState('');
  const [seedArtist, setSeedArtist] = useState('');
  const [seedTrack, setSeedTrack] = useState('');
  const [owner, setOwner] = useState('');
  const [step, setStep] = useState(1);
  const [animationDirection, setAnimationDirection] = useState('forward');

  useEffect(() => {
    if (step === 4) {
      setNumSongs((prevNumSongs) => prevNumSongs || 10);
    }
  }, [step, setNumSongs]);

  useEffect(() => {
    // read session cookie to get user session data
    const cookieData = document.cookie
      .split(';')
      .find(cookie => cookie.startsWith('userSessionData='));
    console.log(cookieData);
    if (cookieData) {
      const userData = JSON.parse(cookieData.split('=')[1]);
      // send user ID to backend to retrieve display name
      fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/token_to_username?token=${userData}`)
        .then(response => response.json())
        .then(data => setOwner(data));
    }
    else {
      setOwner("guest");
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (step !== 6) {
      return;
    }

    // Check if all inputs are filled
    if (!genre || !mood || !numSongs) {
      alert('Please fill out the parameters');
      return;
    }

    // Generate playlist name
    const playlistName = playlistname ? playlistname : `${mood} ${genre}`;

    try {
      // Send a POST request to the Flask API
      const response = await fetch('https://jam-gen-backend-t6vk3.ondigitalocean.app/api/submit-genre', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ genre, playlistname: playlistName, popularity, mood, numSongs, seedArtist, seedTrack, owner }),
      });

      // Check if the response is OK
      if (response.ok) {
        const responseData = await response.json();
        console.log("Response data:", responseData);
        setGenre('');
        setPlaylistName('');
        alert(`Playlist: "${playlistName}" created successfully!`);
        // route to /output-page
        window.location.href = `/output-page`;
      } else {
        const errorData = await response.json();  // Parse the error response
        console.error('Error creating the playlist, please fill out parameters:', errorData);  // Log the error response
        alert('Error creating the playlist, please fill out parameters.');
      }
    } catch (error) {
      console.error('Error in handleSubmit:', error);
      console.error('Response:', error.response);
      alert('Error creating the playlist.');
    }
  };

  const nextStep = () => {
    if (step === 1 && !genre) {
      alert('Please select a genre');
      return;
    } else if (step === 3 && !mood) {
      alert('Please select a mood');
      return;
    } else if (step === 4 && !numSongs) {
      alert('Please enter the number of songs');
      return;
    }

    setAnimationDirection(''); // Reset animation direction
    setAnimationDirection('forward'); // Set the desired animation direction
    setStep(step + 1);
  };

  const prevStep = () => {
    setAnimationDirection(''); // Reset animation direction
    setAnimationDirection('backward'); // Set the desired animation direction
    setStep(step - 1);
  };

  const renderStep = () => {
    const stepClass = animationDirection === 'forward' ? 'slide-forward' : 'slide-backward';


    switch (step) {
      case 1:
        return (
          <div key={step} className={`step ${stepClass}`}>
            <p className="Text-header">What Genre are we looking for?</p>
            {/* Genre input */}
            <select
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              className="InputQ"
              required
            >
              <option value="">Genre</option>
              {["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music", "random"].map((genre) => (
                <option key={genre} value={genre}>{genre.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</option>
              ))}
            </select>
            <button onClick={nextStep} className="NextButtonQ">Next</button>
          </div>
        );
      case 2:
        return (
          <div key={step} className={`step ${stepClass}`}>
            <p className="Text-header">How Popular are we talking?</p>
            <button onClick={prevStep} className="NextButtonQ">Back</button>
            <input
              type="range"
              min="0"
              max="100"
              step="1"
              value={popularity}
              onChange={(e) => {
                const value = e.target.value;
                if (value === '' || (parseInt(value) >= 0 && parseInt(value) <= 100)) {
                  setPopularity(value);
                  // handleSubmit(e); // Trigger handleSubmit when the slider is changed
                }
              }}
              className="InputQ"
            />
            <span className="slider-value">{popularity}</span>
            <button onClick={nextStep} className="NextButtonQ">Next</button>
          </div>
        );
      case 3:
        return (
          <div key={step} className={`step ${stepClass}`}>
            <p className="Text-header">What Mood should you be feeling?</p>
            <button onClick={prevStep} className="NextButtonQ">Back</button>
            <select
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              className="InputQ"
              required
            >
              <option value="">Select mood</option>
              <option value="happy">Happy</option>
              <option value="party">Party</option>
              <option value="chill">Chill</option>
              <option value="focus">Focus</option>
              <option value="sad">Sad</option>
              <option value="sleep">Sleep</option>
              <option value="motivated">Motivated</option>
              <option value="relax">Relax</option>
              <option value="upbeat">Upbeat</option>
              <option value="romantic">Romantic</option>
              <option value="energetic">Energetic</option>
              <option value="calm">Calm</option>
              <option value="inpirational">Inspirational</option>
              <option value="confident">Confident</option>
              <option value="random">Random</option>

            </select>
            <button onClick={nextStep} className="NextButtonQ">Next</button>
          </div>
        );
      case 4:
        return (
          <div key={step} className={`step ${stepClass}`}>
            <p className="Text-header">Just how many Songs do you want?</p>
            <button onClick={prevStep} className="NextButtonQ">Back</button>
            <input
              type="range"
              min="1"
              max="20"
              step="1"
              value={numSongs}
              onChange={(e) => setNumSongs(e.target.value)}
              className="InputQ"
              required
            />
            <span className="slider-value">{numSongs}</span>
            <button onClick={nextStep} className="NextButtonQ">Next</button>
          </div>
        );
      case 5:
        return (
          <div key={step} className={`step ${stepClass}`}>
            <p className="Text-header">Optionally add any references to base the playlist on</p>
            <button onClick={prevStep} className="NextButtonQ">Back</button>
            <input
              type="text"
              placeholder="Seed Artist"
              value={seedArtist}
              onChange={(e) => setSeedArtist(e.target.value.slice(0, 50))}
              className="InputQ"
              maxLength={50}
            />
            <input
              type="text"
              placeholder="Seed Track"
              value={seedTrack}
              onChange={(e) => setSeedTrack(e.target.value.slice(0, 50))}
              className="InputQ"
              maxLength={50}
            />
            <button onClick={nextStep} className="NextButtonQ">Next</button>
          </div>
        );
      case 6:
        return (
          <div key={step} className={`step ${stepClass}`}>
            <p className="Text-header">Give your Playlist a Name! (Or have one generated)</p>
            <button onClick={prevStep} className="NextButtonQ">Back</button>
            <input
              type="text"
              placeholder="Playlist Name"
              value={playlistname}
              onChange={(e) => setPlaylistName(e.target.value)}
              className="InputQ"
              maxLength={30}
            />
            <button type="submit" className="SubmitButtonQ">Submit</button>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {renderStep()}
    </form>
  );
}

export default PlaylistForm;
