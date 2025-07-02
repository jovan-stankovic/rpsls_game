import React, {useEffect, useState} from 'react';
import {getChoices, getScoreboard, playGameRound, refreshAccessToken, resetScoreboard,} from '../services.js';
import AuthForm from './AuthForm.jsx';
import GameResult from './GameResult.jsx';
import Scoreboard from './Scoreboard.jsx';
import ChoiceButton from './ChoiceButton.jsx';
import GameRules from './GameRules.jsx';

function Game() {
  const [choices, setChoices] = useState([]);
  const [scoreboard, setScoreboard] = useState([]);
  const [gameResult, setGameResult] = useState(null);
  const [tokens, setTokens] = useState({ access_token: '', refresh_token: '' });
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const refreshToken = async () => {
    try {
      const response = await refreshAccessToken(tokens.refresh_token);
      setTokens((prevTokens) => ({
        ...prevTokens,
        access_token: response.access_token,
      }));
      return response.access_token;
    } catch (error) {
      console.error("Error refreshing token:", error);
      handleLogout();
      return null;
    }
  };

  const fetchWithRetry = async (requestFunc) => {
    try {
      return await requestFunc(tokens.access_token);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        const newAccessToken = await refreshToken();
        if (newAccessToken) {
          return await requestFunc(newAccessToken);
        }
      }
      throw error;
    }
  };

  useEffect(() => {
    if (tokens.access_token) {
      setIsAuthenticated(true);
    }
  }, [tokens]);

  useEffect(() => {
    if (isAuthenticated && tokens.access_token) {
      const fetchChoices = async () => {
        try {
          const choices = await fetchWithRetry((token) => getChoices(token));
          setChoices(choices);
        } catch (error) {
          console.error('Error fetching choices:', error);
        }
      };

      const fetchScoreboard = async () => {
        try {
          const scoreboard = await fetchWithRetry((token) => getScoreboard(token));
          setScoreboard(scoreboard.slice(0, 10));
        } catch (error) {
          console.error('Error fetching scoreboard:', error);
        }
      };

      fetchChoices();
      fetchScoreboard();
    }
  }, [isAuthenticated, tokens]);

  const handleChoiceClick = async (choiceId) => {
    try {
      const result = await fetchWithRetry((token) =>
        playGameRound(choiceId, token)
      );
      setGameResult(result);

      const updatedScoreboard = await fetchWithRetry((token) =>
        getScoreboard(token)
      );
      setScoreboard(updatedScoreboard.slice(0, 10));
    } catch (error) {
      console.error('Error playing game round:', error);
    }
  };

  const handleResetScoreboard = async () => {
    try {
      await fetchWithRetry((token) => resetScoreboard(token));
      setScoreboard([]);
    } catch (error) {
      console.error('Error resetting scoreboard:', error);
    }
  };

  const handleLogout = () => {
    setTokens({ access_token: '', refresh_token: '' });
    setIsAuthenticated(false);
    window.location.reload();
  };

  return (
    <div className="app-container">
      {!isAuthenticated ? (
        <AuthForm setTokens={setTokens} setIsAuthenticated={setIsAuthenticated} />
      ) : (
        <div className="game-wrapper">
          <div className="sidebar">
            <GameRules />
            <button className="logout-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
          <div className="game-area">
            <h1>Rock-Paper-Scissors-Lizard-Spock</h1>
            {gameResult && <GameResult gameResult={gameResult} />}
          </div>
          <div className="scoreboard-container">
            <Scoreboard
              scoreboard={scoreboard}
              handleResetScoreboard={handleResetScoreboard}
            />
          </div>
        </div>
      )}
      <div className="choice-buttons-container">
        {choices.map((choice) => (
          <ChoiceButton key={choice.id} choice={choice} onClick={handleChoiceClick} />
        ))}
      </div>
    </div>
  );
}

export default Game;
