import React from 'react';
import './PlaylistList.css';

const PlaylistList = ({ songList }) => {
  const numSongs = songList.length / 9;
  const songGroups = Array.from({ length: numSongs }, (_, i) =>
    songList.slice(i * 9, (i + 1) * 9)
  );

  const colors = ['#003840', '#005A5B'];


  const getPopularityLabel = (popularity) => {
    if (popularity < 50) {
      return 'Low Popularity';
    } else if (popularity >= 50 && popularity < 80) {
      return 'Mid Popularity';
    } else {
      return 'High Popularity';
    }
  };

  const formatSongName = (songName) => {
    return songName.replace(/([(\-.\u0080-\uFFFF]).*$/, '').trim();
  }

  const formatAlbum = (album) => {
    return album.replace(/([(\-.\u0080-\uFFFF]).*$/, '').trim();
  }

  return (
    <ul className="playlist-list">
      {songGroups.map((group, index) => (
        <li key={index} className="song-group">
          <a href={group[6]} target="_blank" rel="noopener noreferrer" className="song-group-link">
            <div className="song-group-content">
              <div className="album-art">
                <img src={group[7]} alt="Album Art" />
              </div>
              <div className="song-info">
                <p className="song-name" style={{ color: colors[index % 2] }}> {formatSongName(group[0])}</p>
                <p className="album" style={{ color: colors[(index + 1) % 2] }}> {formatAlbum(group[5])}</p>
                <p className="artist" style={{ color: colors[index % 2] }}> {group[1]}</p>
                <p className="popularity" style={{ color: colors[(index + 1) % 2] }}>
                  {getPopularityLabel(group[3])}
                </p>
                <p className="explicitness" style={{ color: colors[index % 2] }}>
                  {group[4] === 'True' ? 'Explicit' : 'Clean'}
                </p>
                <p className="duration" style={{ color: colors[(index + 1) % 2] }}> {group[2]}</p>
                {/* <p className="uri" style={{ color: colors[index % 2] }}> {group[9]}</p> */}
              </div>
            </div>
          </a>
        </li>
      ))}
    </ul>
  );
};

export default PlaylistList;