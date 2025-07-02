import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Call to retrieve all game choices
export const getChoices = async (accessToken) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/choices`, {
      headers: { Authorization: `${accessToken}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching choices:', error);
    throw error;
  }
};

// Call to retrieve one of game choices
export const getRandomChoice = async (accessToken) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/choice`, {
      headers: { Authorization: `${accessToken}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching random choice:', error);
    throw error;
  }
};

// Call to play a game round
export const playGameRound = async (playerChoice, accessToken) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/play`,
      { player: playerChoice },
      {
        headers: { Authorization: `${accessToken}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error playing game round:', error);
    throw error;
  }
};

// Call to get player's scoreboard
export const getScoreboard = async (accessToken) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/scoreboard`, {
      headers: { Authorization: `${accessToken}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching scoreboard:', error);
    throw error;
  }
};

// Call to reset player's scoreboard
export const resetScoreboard = async (accessToken) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/scoreboard/reset`, {}, {
      headers: { Authorization: `${accessToken}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error resetting scoreboard:', error);
    throw error;
  }
};

// Call to register a new player
export const registerPlayer = async (name, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/register`, { name, password });
    return response.data;
  } catch (error) {
    console.error('Error registering player:', error);
    throw error;
  }
};

// Call to log in a player
export const loginPlayer = async (name, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, { name, password });
    return response.data;
  } catch (error) {
    console.error('Error logging in player:', error);
    throw error;
  }
};

// Call to refresh access token
export const refreshAccessToken = async (refreshToken) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/refresh`, { refresh_token: refreshToken });
    return response.data;
  } catch (error) {
    console.error('Error refreshing access token:', error);
    throw error;
  }
};
