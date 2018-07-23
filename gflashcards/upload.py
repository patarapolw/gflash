from IPython.display import Image
import requests
import json
from pathlib import Path

import sys
try:
    from PIL import ImageGrab
except ImportError:
    import subprocess


with open('user/imgur.json') as f:
    imgur = json.load(f)


def save_image_from_clipboard():
    filename = 'clipboard.png'

    if sys.platform in ["win32", "darwin"]:
        im_data = ImageGrab.grabclipboard()
        im_data.save(filename)
    else:
        with open(filename, 'wb') as f:
            subprocess.call(['xclip', '-se', 'c', '-t', 'image/png', '-o'], stdout=f)

    return save_image_from_file(filename)


def save_image_from_file(filename: str):
    headers = {
        'Authorization': 'Client-ID {}'.format(imgur['Client-ID'])
    }
    data = {
        'image': Path(filename).read_bytes()
    }
    r = requests.post('https://api.imgur.com/3/image', headers=headers, data=data)

    img_url = r.json()['data']['link']
    print(img_url)

    return Image(img_url)
