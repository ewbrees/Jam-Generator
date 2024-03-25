import { FaTrash } from 'react-icons/fa';
import React, { useState, useEffect } from 'react';
import PlaylistList from './PlaylistList';
import './OutputPage.css';
import Navbar from './Navbar';

const OutputPage = () => {
  const [songList, setSongList] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState('');
  const [selectedPlaylistId, setSelectedPlaylistId] = useState('');
  const [owner, setOwner] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // read session cookie to get user session data
    const cookieData = document.cookie
      .split(';')
      .find(cookie => cookie.startsWith('userSessionData='));
    if (cookieData) {
      const userData = JSON.parse(cookieData.split('=')[1]);
      // send user ID to backend to retrieve display name
      fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/token_to_username?token=${userData}`)
        .then(response => response.json())
        .then(data => {
          setOwner(data);
          setIsLoggedIn(true); // User is logged in
        })
        .catch(error => {
          console.error('Error fetching user data from backend:', error);
        });
    } else {
      setIsLoggedIn(false); // User is logged out
    }
  }, []);

  useEffect(() => {
    if (owner) {
      // Fetch all playlists created by the user
      fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/api/get_data_by_owner?owner=${owner}`, {
        method: 'GET'
      })
        .then(response => response.json())
        .then(data => {
          setPlaylists(data);
          if (data.length > 0) {
            // Call handlePlaylistClick with the name of the first playlist to update the state
            handlePlaylistClick(data[0].playlist_id);
          }
        })
        .catch(error => {
          console.error('Error fetching user playlists from backend:', error);
        });
    }
  }, [owner]);

  const handlePlaylistClick = (playlistId) => {
    // Fetch backend data for the specified playlist using the playlistName parameter
    fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/api/get_data_by_id?Id=${playlistId}`, {
      method: 'GET'
    })
      .then(response => response.json())
      .then(data => {
        // Extract the song_list from the backend response and update the state
        setSongList(data[0].song_list.split('|| '));
        setSelectedPlaylist(data[0].playlist_name);
        setSelectedPlaylistId(data[0].playlist_id)
      })
      .catch(error => {
        console.error('Error fetching playlist data from backend:', error);
      });
  };
  const [displayName, setDisplayName] = useState('');

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
        });
    }
  }, []);

  const handleSaveClick = async (playlist_id, playlist_name) => {
    try {
      const cookieData = document.cookie
        .split(';')
        .find((cookie) => cookie.startsWith('userSessionData='));

      const userData = JSON.parse(cookieData.split('=')[1]);
      const response = await fetch('https://jam-gen-backend-t6vk3.ondigitalocean.app/api/save-playlist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playlist_id: playlist_id, playlist_name: playlist_name, token: userData, song_list: songList.join(', ') }),
      });

      if (!response.ok) {
        throw new Error('Failed to save playlist');
      }

      // Display a success message to the user
      alert('Successfully saved playlist to Spotify');

    } catch (error) {
      alert('Did not save playlist to Spotify, try connecting your account again');
      // Handle the error appropriately (e.g., show an error message to the user)
    }
  };

  const handleDeleteClick = (playlistId) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this playlist? This action cannot be undone.");
    if (!confirmDelete) {
      return;
    }
    // Send a DELETE request to the backend API to delete the playlist
    fetch(`https://jam-gen-backend-t6vk3.ondigitalocean.app/api/delete_data_by_id?Id=${playlistId}`, {
      method: 'GET'
    })
      .then(response => response.json())
      .then(data => {
        // Handle the success response
        console.log('Playlist successfully deleted:', data.message);
        // Perform any necessary actions after the playlist is deleted
        window.location.reload()
      })
      .catch(error => {
        console.error('Error deleting playlist:', error);
      });
  };




  return (
    <div className='Output-container'>
      <div className='Sidebar'>
        <h3 style={{ marginLeft: '5%' }}>
          {displayName ? `${displayName}'s Playlists` : "Guest's Playlists"}
        </h3>
        <ul style={{ marginBottom: "10%" }}>
          {playlists.map(playlist => (
            <li key={playlist.playlist_id}>
              <button
                style={{ display: 'inline-flex', alignItems: 'center' }}
                onClick={() => handlePlaylistClick(playlist.playlist_id)}
              >
                {playlist.playlist_name}
              </button>
              <FaTrash
                className="TrashIcon"
                style={{ marginLeft: '2%', color: '#02A676' }}
                onClick={() => handleDeleteClick(playlist.playlist_id)}
              />
            </li>
          ))}
        </ul>
      </div>
      );


      <div className='Output-header'>
        <Navbar />
        <h1 className='Main-text'>
          {selectedPlaylist ? (
            <h2 className='Selected-playlist'>{selectedPlaylist}</h2>
          ) : playlists.length > 0 ? (
            <h2 className='Selected-playlist'>{playlists[0].playlist_name}</h2>
          ) : (
            <p>Select Playlist</p>
          )}

          {isLoggedIn ? (
            <button className='SaveButton' onClick={() => handleSaveClick(selectedPlaylistId, selectedPlaylist)}>
              Save to Spotify
            </button>
          ) : (
            <p>Login to save to Spotify</p>
          )}

          <div className='Song-output'>
            <PlaylistList songList={songList} />
          </div>
        </h1>
      </div>
    </div>
  );
};

export default OutputPage;