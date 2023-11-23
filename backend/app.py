from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import aiohttp
from PIL import Image
from io import BytesIO
import pytesseract
from pydantic import BaseModel
import json

class TextSnippet(BaseModel):
    id: int
    extracted_text: str

app = Flask(__name__)

async def extract_text_from_image(session, url, id):
    async with session.get(url) as response:
        img_data = await response.read()
        text = pytesseract.image_to_string(Image.open(BytesIO(img_data)))
        return {"id": id, "extracted_text": text}

@app.route('/extract-text', methods=['POST'])
def extract_text():
    url = request.json['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    images = soup.find_all('img')
    image_urls = [urljoin(url, img.get('src')) for img in images if img.get('src')]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def process_images():
        async with aiohttp.ClientSession() as session:
            tasks = [extract_text_from_image(session, img_url, i) for i, img_url in enumerate(image_urls)]
            return await asyncio.gather(*tasks)

    image_texts = loop.run_until_complete(process_images())

    with open('screenshots.json', 'w') as file:
        json.dump(image_texts, file)

    return jsonify({'message': 'Text extracted successfully', 'data': image_texts})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
