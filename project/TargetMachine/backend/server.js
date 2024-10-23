const express = require('express');
const db = require('./database');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 5050;

app.use(cors({
  origin: 'http://34.224.51.201',  // Update to your actual frontend URL or public IP
}));

// Serve static files from the React app (the client build folder)
app.use(express.static(path.join(__dirname, '../frontend/dist')));

// Middleware to parse JSON request bodies
app.use(express.json());

// Handle login POST request
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  // Simulated login check
  if (username === 'admin' && password === 'password') {
    res.status(200).json({ message: 'Login Success!' });
    console.log(res);
  } else {
    res.status(401).json({ message: 'Invalid Credentials' });
  }
});

// Catch-all route to serve the React frontend
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dist', 'index.html'));
});

// Start the server
app.listen(port, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${port}`);
});
