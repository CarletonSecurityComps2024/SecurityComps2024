const express = require('express');
const db = require('./database');
const path = require('path');
const cors = require('cors');
const base64 = require('base-64');
const axios = require('axios');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();

// Middleware to parse req bodies
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Serve static files from the React app (the client build folder)
app.use(express.static(path.join(__dirname, '../frontend/dist')));

const VALID_USERNAME = 'admin';
const VALID_PASSWORD = 'password;'
const PORT = 5050;
const IPCounts = {}

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

// Decode Basic Auth Credentials 
const decodeCredentials = (authHeader) => {
	const encodedCredentials = authHeader.trim().replace(/Basic\s+/i, '');
	const decodedCredentials = base64.decode(encodedCredentials);
	return decodedCredentials.split(';');
}

const validateIP = async (requestIP, res) => {
	try {
		// Query to check if IP is in blocked_ips
		const { rowCount } = await db.query(
		'SELECT 1 FROM blocked_ips WHERE ip_address = $1',
		[requestIP]);

		// If IP is found in blocked_ips, deny login request
		if (rowCount > 0) {
			return res.status(403).json({ message: 'Access Denied' });
		} 
	} catch (error) {
		console.error('Database query error: ', error);
		res.status(500).json({message: 'Internal Server Error'});
	}
}

const getRandomCaptcha = () => {
	try{
		const files = fs.readdirSync('./CaptchaDataset');
		
		if (files.length === 0) {
			throw new Error('No files found in Captcha directory.');
		}

		const randomCaptcha = files[Math.floor(Math.random() * files.length)];
		console.log("random captcha: ", randomCaptcha);
		return randomCaptcha;
	} catch(error) {
		console.error('Error reading directory: ', error);
	}
}

getRandomCaptcha();

// Middleware for HTTP Basic Auth with CAPTCHA
const authWithCaptchaMiddleware = async (req, res, next) => {
	const authHeader = req.headers.authorization || '';
	const [username, password] = decodeCredentials(authHeader);
	const requestIP = req.ip;
	
	// Check if address IP is blocked; Else, keep track to prevent spam requests
	validateIP(requestIP);
	handleNewIP(requestIP, res);
	
	//

}


// Handle login POST request
app.post('/login', authWithCaptchaMiddleware,(req, res) => {

  	// Simulated login check
  	if (username === VALID_USERNAME && password === VALID_PASSWORD) {
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
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${PORT}`);
});
