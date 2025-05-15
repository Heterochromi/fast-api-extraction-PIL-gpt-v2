from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
from chunk_get_PIL_V2 import splitHtml

app = FastAPI()


@app.post("/split_html")
async def splitHtmlSections(file: UploadFile = File(...), lang: str = "en"):
    # time.sleep(2)
    content = await file.read()
    html_content = content.decode("utf-8")
    print(html_content)
    processed_html_output = splitHtml(html_content, lang)

    # Directly return the HTML string as a response, prompting download.
    headers = {
        "Content-Disposition": "attachment; filename=processed_document.html"
    }
    return HTMLResponse(content=processed_html_output, headers=headers)




