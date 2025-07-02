import React from 'react';
import {CHOICE_MAP} from '../Constants.jsx';

function Scoreboard({ scoreboard, handleResetScoreboard }) {
  return (
    <div>
      <h2>Scoreboard</h2>
      <table className="scoreboard-table">
        <thead>
          <tr>
            <th>Result</th>
            <th>Player's Choice</th>
            <th>Computer's Choice</th>
          </tr>
        </thead>
        <tbody>
          {scoreboard.map((score, index) => (
            <tr key={index}>
              <td>{score.result}</td>
              <td>{CHOICE_MAP[score.player_choice]}</td>
              <td>{CHOICE_MAP[score.computer_choice]}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleResetScoreboard}>Reset Scoreboard</button>
    </div>
  );
}

export default Scoreboard;
