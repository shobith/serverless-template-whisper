import torch
from faster_whisper import WhisperModel
import os
import base64
from io import BytesIO

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model
    
    whisper_model = "medium"
    model = WhisperModel(whisper_model, compute_type="int8")

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    mp3BytesString = model_inputs.get('mp3BytesString', None)
    if mp3BytesString == None:
        return {'message': "No input provided"}
    
    mp3Bytes = BytesIO(base64.b64decode(mp3BytesString.encode("ISO-8859-1")))
    with open('input.mp3','wb') as file:
        file.write(mp3Bytes.getbuffer())

    options = dict(task="transcribe", language="en", beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0))

    # Run the model
    segments_raw, info = model.transcribe("input.mp3", **options)
    segments = []
    n_chunks = 0
    for segment_chunk in segments_raw:
        chunk = {}
        chunk["start"] = segment_chunk.start
        chunk["end"] = segment_chunk.end
        chunk["text"] = segment_chunk.text
        segments.append(chunk)
        n_chunks += 1

    output = {"text":''.join([segment["text"] for segment in segments])}
    os.remove("input.mp3")

    # Return the results as a dictionary
    return output
