import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [channels, setChannels] = useState([]);

  const fetchSubscriptions = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/fetch-subscriptions");
      setChannels(response.data);
    } catch (error) {
      console.error("Error fetching subscriptions:", error);
    }
  };

  return (
    <div className="container">
      <h1>YouTubeチャンネル登録一覧</h1>
      <button onClick={fetchSubscriptions}>取得ボタン</button>
      <ul>
        {channels.map((channel, index) => (
          <li key={index}>
            <strong>{channel.title}</strong> - {channel.genre}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
