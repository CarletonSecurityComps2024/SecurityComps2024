const express = require('express');
const db = require('./database');
const path = require('path');
const cors = require('cors');
const base64 = require('base-64');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();

// CORS to connect with frontend
app.use(cors())

// Middleware to parse req bodies
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const VALID_USERNAME = 'admin';
const VALID_PASSWORD = 'password'
const PORT = 5050;
const IPCounts = {}

let VALID_CAPTCHA;
// let count = 0; // FOR TESTING PURPOSES

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

// Check if IP address is blocked or not
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

// Return a random CAPTCHA for log-in authentication
// Return image as a base64 string
const getRandomCaptcha = async () => {
	try{
		const files = fs.readdirSync('./CaptchaDataset'); // Read files
		
		if (files.length === 0) { // Check if dir is found
			throw new Error('No files found in Captcha directory.');
		}

		const randomCaptcha = files[Math.floor(Math.random() * files.length)]; // Select a random CAPTCHA img from dir.
		VALID_CAPTCHA = randomCaptcha.split('.png')[0] // Value of selected CAPTCHA

		const captchaPath = path.join('./CaptchaDataset', randomCaptcha)

		try {
			const data = fs.readFileSync(captchaPath, 'base64'); // Read file as base64
			return data
		} catch (error) {
			throw new Error('Captcha file could not be read. ', error);
		}
	} catch(error) {
		console.error('Error reading directory: ', error);
		throw error;
	}
}

// FOR TESTING PURPOSES
// Return controlled CAPTCHA
const getConstCaptcha = async () => {
	let constCaptcha;
	
	// Return different CAPTCHA after page refresh
	if (count == 2) {
		constCaptcha = '1AJEB.png';
	} else {
		constCaptcha = '1AASX.png';
		count = count + 1;
	}

	VALID_CAPTCHA = constCaptcha.split('.png')[0];

	const captchaPath = path.join('./CaptchaDataset', constCaptcha);

	try {
		const data = fs.readFileSync(captchaPath, 'base64'); // Read file as base64
		return data
	} catch (error) {
		throw new Error('Constant captcha file could not be read. ', error);
	}
}


// GET request to serve login form
app.get('/login', async (req, res) => {
	try {	// Respond with a random CAPTCHA on request
		const captchaData = await getRandomCaptcha();
		res.json({
			captchaImage: captchaData,
		});
	} catch (error) {
		res.status(500).json({message: 'Internal Server Error.'})
	}
});


// Handle login POST request
app.post('/login', async (req, res) => {

	const { username, password, captchaValue } = req.body; // Filter out authentication values
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

	try {
        // Authenticate user
        if (
            username.trim() === VALID_USERNAME &&
            password.trim() === VALID_PASSWORD &&
            captchaValue.trim() === VALID_CAPTCHA
        ) {
            console.log('Login Success!');
            return res.status(200).json({ message: 'Login Success!' });
        }
        console.log('Invalid Credentials');
        res.status(401).json({ message: 'Invalid Credentials' });
    } catch (error) {
        console.error('Error during login:', error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
// app.listen(PORT, 'localhost', () => {
  console.log(`Server running at http://0.0.0.0:${PORT}`);
});
