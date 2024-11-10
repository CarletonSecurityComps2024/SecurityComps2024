import React, { useState, useEffect } from 'react';

const Login: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [captchaValue, setCaptchaValue] = useState<string>('');
  const [captchaImage, setCaptchaImage] = useState<string>('');
  const [loginMessage, setLoginMessage] = useState<string>('');

  const fetchNewCaptcha = async () => {
    console.log('here'
    )
    try {
      const response = await fetch('http://34.224.51.201:5050/login');
      // const response = await fetch('http://localhost:5050/login'); 
      const data = await response.json();
      setCaptchaImage(data.captchaImage);
    } catch (error) {
      console.error('Error fetching CAPTCHA: ', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
        try {
            const response = await fetch('http://34.224.51.201:5050/login');
            // const response = await fetch('http://localhost:5050/login'); 
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setCaptchaImage(data.captchaImage);
            console.log(data.captchaImage)
        } catch (error) {
          console.error('Fetching error:', error);
        };
      }
    fetchData();
  }, []);



  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      // Send a POST request to the backend server
      const response = await fetch('http://34.224.51.201:5050/login', {
      // const response = await fetch(`http://localhost:5050/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password, captchaValue }),
      });

      const data = await response.json();
      console.log("Data: ", data);

      if (response.status === 200) {
        setLoginMessage('Login Success!');
      } else {
        setLoginMessage(data.message || 'Invalid Credentials');
        fetchNewCaptcha(); // Fetch a new CAPTCHA on failure
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
        {captchaImage && (
          <img src={`data:image/jpg;base64,${captchaImage}`} alt="Captcha" />
        )}
        <div>
          <label>CAPTCHA: </label>
          <input
            type="text"
            value={captchaValue}
            onChange={(e) => setCaptchaValue(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>

      {loginMessage && <div>{loginMessage}</div>}
    </div>
  );
};

export default Login;
