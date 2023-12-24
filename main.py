from fastapi import FastAPI
from transformers import pipeline
import urllib.request
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

app = FastAPI()
# Mute tensorflow complaints
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def extract_from_url(url):
    text = ""
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecji) Chrome/35.0.1916.47 Safari/537.36"
        },
    )
    html = urllib.request.urlopen(req)
    parser = BeautifulSoup(html, "html.parser")
    for paragraph in parser.find_all("p"):
        # print(paragraph.text)
        text += paragraph.text
    return text


def process(text):
    summariser = pipeline("summarization", model="t5-small")
    result = summariser(text, max_length=180)
    return result[0]["summary_text"]


@app.post("/url")
async def summarizer_url(url):

    text = extract_from_url(url)
    result = process(text)
    payload = {"summarise": result}
    json_compatible_item_data = jsonable_encoder(payload)
    return JSONResponse(content=json_compatible_item_data)

@app.post("/file")
async def summarizer_file(file):
   
    with open(file, "r", encoding="utf-8") as _f:
        text = _f.read()
    result = process(text)
    payload = {"summarise": result}
    json_compatible_item_data = jsonable_encoder(payload)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/")
async def root():
    return {"messsage": "Hello functions"}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host="0.0.0.0")


def add(x, y):
    return x + y
