from uuid import uuid4
from pathlib import Path
from IPython.display import Image, display

import sys
try:
    from PIL import ImageGrab
except ImportError:
    import subprocess


def save_image_from_clipboard():
    filename = Path('user/clipboard').joinpath(str(uuid4().hex) + '.png')

    if sys.platform in ["win32", "darwin"]:
        im_data = ImageGrab.grabclipboard()
        im_data.save(filename)
    else:
        with filename.open('wb') as f:
            subprocess.call(['xclip', '-se', 'c', '-t', 'image/png', '-o'], stdout=f)

    img = Image(filename=str(filename))
    display(img)

    return filename
