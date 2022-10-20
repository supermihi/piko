import livedata

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live")
def read_live():
    ans = livedata.get_live_data()
    return {k.name: v for k, v in ans.items()}

@app.get("/", response_class=HTMLResponse)
def get_root():
    html = Path('./index.html')
    return html.read_text()