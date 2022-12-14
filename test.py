# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests
from io import BytesIO
import base64
import os

def run(file): 
    # Needs test.mp3 file in directory
    with open(file,'rb') as file:
        mp3bytes = BytesIO(file.read())
    mp3 = base64.b64encode(mp3bytes.getvalue()).decode("ISO-8859-1")

    model_payload = {"mp3BytesString":mp3}

    res = requests.post("http://100.81.121.129:8000/",json=model_payload)

    print(res.text)

files = ["../whisper.cpp/chanakya/one.wav", "../whisper.cpp/chanakya/two.wav", "../whisper.cpp/chanakya/three.wav", "../whisper.cpp/chanakya/four.wav", "../whisper.cpp/chanakya/five.wav", "../whisper.cpp/chanakya/six.wav", "../whisper.cpp/chanakya/seven.wav", "../whisper.cpp/chanakya/eight.wav", "../whisper.cpp/chanakya/nine.wav"]

for f in files:
    run(f)
