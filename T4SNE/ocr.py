import os
import sys
import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
import argparse
import fitz
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--image-path', type = str, default = None)
parser.add_argument('--image-url', type = str, default = None)
parser.add_argument('--pdf-path', type=str, default=None)
args = parser.parse_args()

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

ocr_url = endpoint + "vision/v3.1/ocr"

# Set image_url to the URL of an image that you want to analyze.
if args.image_url is not None:
    image_url = args.image_url
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    data = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, json=data)

elif args.image_path is not None:
    image_path = args.image_path
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)

elif args.pdf_path is not None:
    doc = fitz.open(args.pdf_path)
    pix = doc[0].getPixmap().getImageData(output='JPEG')
    jpg_as_np = np.frombuffer(pix, dtype=np.uint8)
    image = cv2.imdecode(jpg_as_np, flags=1)
    p = args.pdf_path.replace('.pdf', '.jpg')
    cv2.imwrite(p, image)
    image_path = p
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    
else:
    print("Invalid entry. Please try again")
    exit()

response.raise_for_status()

analysis = response.json()

# Extract the word bounding boxes and text.
line_infos = [region["lines"] for region in analysis["regions"]]
word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)

text = ""
for word in word_infos:
    text += word['text'] + " "

print(text)
with open('text.txt', 'w') as f:
	f.write(text)