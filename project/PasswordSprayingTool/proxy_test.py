import requests, asyncio
from apify import Actor

import os
from dotenv import load_dotenv
load_dotenv()
# Get environment variables
APIFY_PROXY_HOSTNAME = os.getenv("APIFY_PROXY_HOSTNAME")
APIFY_PROXY_PORT = os.getenv("APIFY_PROXY_PORT")
APIFY_PROXY_PASSWORD = os.getenv("APIFY_PROXY_PASSWORD")



# Construct the connection string
connection_string = f"http://auto:{APIFY_PROXY_PASSWORD}@{APIFY_PROXY_HOSTNAME}:{APIFY_PROXY_PORT}"

print(connection_string)

async def main():
    async with Actor:
        proxy_configuration = await Actor.create_proxy_configuration(password="apify_proxy_5pOmJ4e3iHevhBYl7FjYFfCbZpj05D30LPms")
        proxy_url = await proxy_configuration.new_url()

        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }

        response = requests.get('https://api.apify.com/v2/browser-info', proxies=proxies)
        print(response.text)

if __name__ == '__main__':
    asyncio.run(main())