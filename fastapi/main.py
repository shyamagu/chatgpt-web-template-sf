from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import simple,order,booksearch,bingsearch,pdfmaster,longconv,surveybot
from fastapi.responses import HTMLResponse
#from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
#app.add_middleware(SessionMiddleware, secret_key="some-random-string")

# /simple
app.include_router(simple.router)

# /order
app.include_router(order.router)

# /booksearch
app.include_router(booksearch.router)

# /bingsearch
app.include_router(bingsearch.router)

# /pdf**
app.include_router(pdfmaster.router)

# /longconv
app.include_router(longconv.router)

# /surveybot
app.include_router(surveybot.router)

# 本当はもっとスマートにやりたい。sveltekitでのbuild成果物のHTMLを返す
@app.get("/basic")
async def basic():
    with open("static/basic.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/demae")
async def demae():
    with open("static/demae.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/book")
async def book():
    with open("static/book.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/bing")
async def bing():
    with open("static/bing.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/pdf")
async def pdf():
    with open("static/pdf.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/long")
async def long():
    with open("static/long.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/survey")
async def survey():
    with open("static/survey.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# staticディレクトリにindex.htmlを置く
app.mount("/", StaticFiles(directory="static", html=True), name="static")
