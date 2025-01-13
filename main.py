from fastapi import FastAPI
from pydantic import BaseModel
from chunk_get_PIL_V2 import get_PIL , get_PIL_ar
from typing import List
from smpc.smpc_section import get_smpc
import time

app = FastAPI()

class LargeString(BaseModel):
    content: List[str] = []

@app.post("/get_pil_ar")
async def get_PL(large_string: LargeString,lang: str = "ar"):
    # time.sleep(2)
    result = get_PIL_ar(large_string.content , lang=lang)
    return result


@app.post("/get_pil_en")
async def get_PL(large_string: LargeString,lang: str = "en"):
    # time.sleep(2)
    result = get_PIL(large_string.content , lang=lang)
    return result



class smpc_section(BaseModel):
    titles: List[str] = []
    content: List[str] = []
    

@app.post("/smpc_section")
async def smpc_section(smpc_section: smpc_section):
    return get_smpc(smpc_section.titles,smpc_section.content)


@app.get("/timeout")
async def get_PL(large_string: LargeString):
    time.sleep(61)
    return {"message": "Timeout"}