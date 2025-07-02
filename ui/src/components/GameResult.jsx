import React from 'react';
import {CHOICE_MAP, IMAGE_MAP} from '../Constants.jsx';

function GameResult({ gameResult }) {
  return (
    <div className="game-area">
      <h2 className="game-result-header">{gameResult.result}</h2>
      {gameResult && (
        <div className="game-result-container">
          <div className="game-result-choice">
            <h3>Your Choice</h3>
            <img
              src={IMAGE_MAP[CHOICE_MAP[gameResult.player_choice].toLowerCase()]}
              alt={CHOICE_MAP[gameResult.player_choice]}
              className="choice-image-result"
            />
          </div>
          <div className="game-result-choice">
            <h3>Computer's Choice</h3>
            <img
              src={IMAGE_MAP[CHOICE_MAP[gameResult.computer_choice].toLowerCase()]}
              alt={CHOICE_MAP[gameResult.computer_choice]}
              className="choice-image-result"
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default GameResult;
