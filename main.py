from fastapi import FastAPI
from pydantic import BaseModel
from chunk_get_PIL import get_PIL
from typing import List
import time

app = FastAPI()

class LargeString(BaseModel):
    content: List[str] = []

@app.post("/get_pil")
async def get_PL(large_string: LargeString,lang: str = "en" or "ar"):
    # time.sleep(2)
    result = get_PIL(large_string.content , lang=lang)
    return result

@app.get("/timeout")
async def get_PL(large_string: LargeString):
    time.sleep(61)
    return {"message": "Timeout"}