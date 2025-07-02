import React from 'react';
import {CHOICE_MAP, IMAGE_MAP} from '../Constants.jsx';

function ChoiceButton({ choice, onClick }) {
  return (
    <img
      src={IMAGE_MAP[choice.name.toLowerCase()]}
      alt={CHOICE_MAP[choice.name.toLowerCase()]}
      onClick={() => onClick(choice.id)}
      className={`choice-image ${choice.name.toLowerCase() === 'spock' ? 'spock' : ''}`}
    />
  );
}

export default ChoiceButton;
