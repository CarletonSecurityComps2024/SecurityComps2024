const express = require('express');
const cors = require('cors');  // Import CORS middleware
const app = express();
const port = 5050;

// Use CORS to allow requests from the frontend (http://localhost:5173)
app.use(cors({
  origin: 'http://localhost:5173',  // Allow requests from this origin (frontend)
}));

// Middleware to parse JSON request bodies
app.use(express.json());

// Handle login POST request
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  // Simulated login check
  if (username === 'admin' && password === 'password') {
    console.log(`Correct Password!`)
    res.status(200).json({ message: 'Login Success!' });
  } else {
    console.log(`Status 401: Invalid Credentials`)
    res.status(401).json({ message: 'Invalid Credentials' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
