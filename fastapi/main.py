from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import simple,order
from fastapi.responses import HTMLResponse

app = FastAPI()

# /simple
app.include_router(simple.router)

# /order
app.include_router(order.router)

# /demae のHTMLを返す
@app.get("/demae")
async def demae():
    with open("static/demae.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# staticディレクトリにindex.htmlを置く
app.mount("/", StaticFiles(directory="static", html=True), name="static")

