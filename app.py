from flask import Flask, jsonify, Response
import requests
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

IMAGE_URL = 'https://coreclub.in/frames/'

def fetch_image_list():
    response = requests.get(IMAGE_URL)
    if response.status_code == 200:
        images = [line.split('"')[1] for line in response.text.splitlines() if 'href="' in line and line.split('"')[1].endswith(('jpg', 'jpeg', 'png', 'gif'))]
        return images
    else:
        return None

@app.route('/images', methods=['GET'])
def list_images():
    try:
        images = fetch_image_list()
        if images is not None:
            return jsonify(images)
        else:
            return jsonify({'error': 'Failed to retrieve images from the server'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images/count', methods=['GET'])
def count_images():
    try:
        images = fetch_image_list()
        if images is not None:
            return jsonify({'count': len(images)})
        else:
            return jsonify({'error': 'Failed to retrieve images from the server'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    try:
        image_url = os.path.join(IMAGE_URL, filename)
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img_io = BytesIO()
            img.save(img_io, 'JPEG')
            img_io.seek(0)
            return Response(img_io, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
