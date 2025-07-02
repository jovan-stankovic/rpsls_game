import React, {useState} from 'react';
import {loginPlayer, registerPlayer} from '../services';

function AuthForm({ setTokens, setIsAuthenticated }) {
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [feedback, setFeedback] = useState('');

  const handleLoginOrRegister = async (isRegistering) => {
    try {
      let response;
      if (isRegistering) {
        response = await registerPlayer(name, password);
        setFeedback(`Registered successfully as ${response.name}.`);
      }

      response = await loginPlayer(name, password);
      if (response.access_token) {
        setTokens({
          access_token: response.access_token,
          refresh_token: response.refresh_token,
        });
        setIsAuthenticated(true);
      }
    } catch (error) {
      setFeedback('Login/Registration failed.');
      console.error('Error during auth:', error);
    }
  };

  return (
    <div className="auth-form">
      <h2>{isRegister ? 'Sign Up' : 'Sign In'}</h2>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={() => handleLoginOrRegister(isRegister)}>
        {isRegister ? 'Sign Up' : 'Sign In'}
      </button>
      <p>
        {isRegister ? 'Already have an account? ' : 'Don’t have an account? '}
        <span onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? 'Sign In' : 'Sign Up'}
        </span>
      </p>
      {feedback && <p>{feedback}</p>}
    </div>
  );
}

export default AuthForm;
