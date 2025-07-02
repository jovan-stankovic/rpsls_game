import React from 'react';
import rulesImage from '../assets/rules.png';

function GameRules() {
  return (
    <div className="game-rules-container">
      <img src={rulesImage} alt="Game Rules" className="game-rules-image" />
      <p className="game-rules-text">
          Rock crushes Scissors  <br/>
          Scissors cuts Paper<br/>
          Paper covers Rock<br/>
          Rock crushes Lizard<br/>
          Lizard poisons Spock<br/>
          Spock smashes Scissors<br/>
          Scissors decapitates Lizard<br/>
          Lizard eats Paper<br/>
          Paper disproves Spock<br/>
          Spock vaporizes Rock<br/>
      </p>
    </div>
  );
}

export default GameRules;
