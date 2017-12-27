import base64
import uuid
import os
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image

filePath = './downloads/'
os.makedirs(filePath, exist_ok=True)


def getImgPlain(dataUri):
    head, data = dataUri.split(',', 1)
    file_ext = head.split(';')[0].split('/')[1]
    return BytesIO(base64.b64decode(dataUri.split(',')[1]))


def stitchAndSaveImage(pieces):
    images = map(Image.open, pieces)
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights)

    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    images = map(Image.open, pieces)
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_im.save(filePath + str(uuid.uuid4()) + '.jpg')
    print("Saved new img to" + filePath + str(uuid.uuid4()) + '.jpg')


url = "https://imagetheftprevention.azurewebsites.net/home"

r = requests.get(url)

soup = BeautifulSoup(r.content, "lxml")

imgGroups = soup.find_all("div", {"class": "image-container"})

for img in imgGroups:
    pieces = []
    for imgPiece in img.find_all("img"):
        pieces.append(getImgPlain(imgPiece.get("src")))
    stitchAndSaveImage(pieces)
