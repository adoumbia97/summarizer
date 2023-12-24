from transformers import pipeline
from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn

generator=pipeline("text-generation", model='gpt2')

app=FastAPI()
class Body(BaseModel):
    text:str

@app.get('/')
def root():
    return("<h1> Hello from DOUMBIA </h1>")

@app.post('/generate')
def predict(body: Body):
    results=generator(body.text, max_length=35, num_return_sequences=1)
    return results[0]

if __name__=='__main__':
     uvicorn.run(app, port=8080, host="0.0.0.0")

def add(x,y):
    return x+y