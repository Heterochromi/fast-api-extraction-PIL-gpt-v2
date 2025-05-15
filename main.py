from fastapi import FastAPI
from pydantic import BaseModel
from chunk_get_PIL_V2 import splitHtml_ar , splitHtml_en
from typing import List
import time

app = FastAPI()

class LargeString(BaseModel):
    content: List[str] = []

@app.post("/split_sections_en")
async def splitHtml_ar(large_string: LargeString):
    # time.sleep(2)
    result = splitHtml_en(large_string.content)
    return result


@app.post("/get_pil_en")
async def get_PL(large_string: LargeString):
    # time.sleep(2)
    result = splitHtml_ar(large_string.content)
    return result



@app.get("/timeout")
async def get_PL(large_string: LargeString):
    time.sleep(61)
    return {"message": "Timeout"}