import requests
from bs4 import BeautifulSoup
import time

# Function to check stock status
def check_stock(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for the "Out of Stock" text in the specified div
    stock_status_div = soup.find('div', class_='m-0 leading-none py-fm8 px-fm16 md:py-f8 md:px-f20 rounded-full bg-white text-black border-[1px] border-[#000000] fmtext-10 md:ftext-10 inline-flex justify-center items-center gap-fm8 md:gap-f8 w-full md:w-auto')
    if stock_status_div and 'Out of Stocks' in stock_status_div.get_text():
        return False
    return True

# Function to send notification to Discord
def send_discord_message(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# URL of the item page
url = 'https://store.analogue.co/products/analogue-3d-black'

# Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/1323133487774961765/q3vvTsrD0zehHCsrT8X8uqpQkvGFtSElqwjTAjcUcUsBsFCmwhk_04Luqx8kM4WNkC_P'  # Replace with your Discord webhook URL

# Check stock every minute
while True:
    in_stock = check_stock(url)
    if in_stock:
        send_discord_message(discord_webhook_url, f'The item is back in stock! Check it out here: {url}')
        break
    time.sleep(60)  # Wait for a minute before checking again
