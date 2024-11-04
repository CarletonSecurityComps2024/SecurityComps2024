const express = require('express');
const db = require('./database');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 5050;
const IPCounts = {}

// Serve static files from the React app (the client build folder)
app.use(express.static(path.join(__dirname, '../frontend/dist')));

// Middleware to parse JSON request bodies
app.use(express.json());


const handleNewIP = async (ip, res) => {
    if (IPCounts[ip]) {
        if (IPCounts[ip] > 25) {
	    try {
            	await db.query(
                    'INSERT INTO blocked_ips (ip_address) VALUES ($1) ON CONFLICT (ip_address) DO NOTHING',
                    [ip]
            	);
            	console.log(`IP Address ${ip} has been added to the blocked_ips table.`);
            } catch (error) {
            	console.error('Error adding IP to blocked_ips:', error);
            	return res.status(500).json({ message: 'Internal Server Error' });
            }	
	} else {
	    IPCounts[ip] += 1;
	}
    } else {
        IPCounts[ip] = 1;
    }
}


// Handle login POST request
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const requestIP = req.ip;

  try {
    // Query to check if IP is in blocked_ips
    const { rowCount } = await db.query(
      'SELECT 1 FROM blocked_ips WHERE ip_address = $1',
      [requestIP]
    );

    // If IP is found in blocked_ips, return an error
    if (rowCount > 0) {
      return res.status(403).json({ message: 'Access Denied' });
    } 
  } catch (error) {
    console.error('Database query error: ', error);
    res.status(500).json({message: 'Internal Server Error'});
  }

  handleNewIP(requestIP, res);

  // Simulated login check
  if (username === 'admin' && password === 'password') {
    console.log(`Correct Password!`)
    res.status(200).json({ message: 'Login Success!' });
  } else {
    console.log(`Status 401: Invalid Credentials`)
    res.status(401).json({ message: 'Invalid Credentials' });
  }
  console.log(res.statusCode)
});

// Catch-all route to serve the React frontend
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dist', 'index.html'));
});

// Start the server
app.listen(port, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${port}`);
});
