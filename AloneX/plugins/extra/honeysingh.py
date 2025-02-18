from pyrogram import Client, filters
import requests
import random
from AloneX import app

UNSPLASH_ACCESS_KEY = "oBw-gH0Pt6e4SqjhTM65yYOrlIGgz-Jrnj8WjCZIn_0"
UNSPLASH_QUERY = "Yo Yo Honey Singh"

@app.on_message(filters.command("honey") & filters.private)
async def send_random_image(client, message):
    url = f"https://api.unsplash.com/search/photos?page=1&query={UNSPLASH_QUERY}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            random_image = random.choice(data["results"])["urls"]["full"]
            await message.reply_photo(random_image, caption="Here is a random Honey Singh image for you!")
        else:
            await message.reply_text("No images found for the query.")
    else:
        await message.reply_text("Failed to fetch images. Please try again later.")
