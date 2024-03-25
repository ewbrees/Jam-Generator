// example of how to pull data from the database and display it on the page, can use this for reference when building the actual playlist page
// generated with chatgpt

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PlaylistList() {
  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    axios.get('/api/playlists')
      .then(response => {
        setPlaylists(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>Playlist List</h1>
      <ul>
        {playlists.map(playlist => (
          <li key={playlist.id}>
            <h2>{playlist.name}</h2>
            <p>Genre: {playlist.genre}</p>
            <p>Owner: {playlist.owner}</p>
            <p>Created at: {playlist.created_at}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PlaylistList;
