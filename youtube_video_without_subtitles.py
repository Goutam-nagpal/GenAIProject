
import requests

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# output = query("uploaded_videos\Amazing Langchain Series With End To End Projects- Prerequisites To Start With [4O1rs7mrNDo].mp3")
# print(output)
