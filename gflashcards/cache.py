import base64
from pathlib import Path


def file_to_base64(filename):
    filename = Path(filename)

    return base64.b64encode(filename.read_bytes()).decode()
