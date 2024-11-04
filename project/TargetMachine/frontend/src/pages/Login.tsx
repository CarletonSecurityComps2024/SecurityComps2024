import React, { useState } from 'react';

const Login: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [loginMessage, setLoginMessage] = useState<string>('');

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      // Send a POST request to the backend server
      const response = await fetch('http://34.224.51.201:5050/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      console.log("Data: ", data);

      if (response.status === 200) {
        setLoginMessage('Login Success!');
      } else {
        setLoginMessage('Invalid Credentials');
      }
    } catch (error) {
      setLoginMessage('An error occurred');
      console.error('Login error:', error);
    }
  };

  return (
    <div>
      <h1>Login Page</h1>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username: </label>
          <input 
            type="text" 
            value={username}
            onChange={(e) => setUsername(e.target.value)} 
          />
        </div>
        <div>
          <label>Password: </label>
          <input 
            type="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)} 
          />
        </div>
        <button type="submit">Login</button>
      </form>

      {loginMessage && <div>{loginMessage}</div>}
    </div>
  );
};

export default Login;
