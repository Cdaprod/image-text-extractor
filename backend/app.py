#!/usr/local/bin python3
# pip install flask streamlit requests BeautifulSoup4 pillow pytesseract pydantic

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from PIL import Image as PILImage
from io import BytesIO
import pytesseract
from pydantic import BaseModel
import json

class TextSnippet(BaseModel):
    id: int
    extracted_text: str

class Image(BaseModel):
    url: str

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    image_data = Image(**request.json)
    response = requests.get(image_data.url)
    soup = BeautifulSoup(response.content, 'html.parser')

    images = soup.find_all('img')
    image_texts = []

    for i, img in enumerate(images):
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            img_response = requests.get(img_url)
            img_data = BytesIO(img_response.content)
            text = pytesseract.image_to_string(PILImage.open(img_data))
            image_texts.append(TextSnippet(id=i, extracted_text=text).dict())

    with open('screenshots.json', 'w') as file:
        json.dump(image_texts, file)

    return jsonify({'message': 'Text extracted successfully', 'data': image_texts})

if __name__ == '__main__':
    app.run(debug=True, port=5001)