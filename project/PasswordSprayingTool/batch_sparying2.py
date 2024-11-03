import asyncio
import aiohttp

url = 'http://50.19.17.226:5050/login'
BATCH_SIZE = 1  # Number of requests per batch

# Function to send a login request
async def send_login_request(session):
    try:
        async with session.post(url, json={
            'username': 'admin',  # Replace these with valid credentials if needed
            'password': 'pa'
        }) as response:
            pass
        print('Response status:', response.status)
    except Exception as error:
        print('Request failed:', error)

# Function to send requests in batches
async def send_requests_in_batches(total_requests):
    async with aiohttp.ClientSession() as session:
        for i in range(0, total_requests, BATCH_SIZE):
            batch_requests = [
                send_login_request(session)
                for _ in range(min(BATCH_SIZE, total_requests - i))
            ]
            
            # Send batch and wait for completion
            await asyncio.gather(*batch_requests)
            print(f'Sent batch of {len(batch_requests)} requests.')


    print(f'Total of {total_requests} requests completed.')

# Specify the number of total requests here
asyncio.run(send_requests_in_batches(1000012))