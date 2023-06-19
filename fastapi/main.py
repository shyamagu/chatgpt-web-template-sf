from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import simple,order,booksearch,bingsearch,pdfmaster,longconv,surveybot,embedding,vsinjection,autonomous
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

# /embedding
app.include_router(embedding.router)

# /vsinjection
app.include_router(vsinjection.router)

# /autonomous
app.include_router(autonomous.router)

# 本当はもっとスマートにやりたい。sveltekitでのbuild成果物のHTMLを返す
@app.get("/basic")
def basic():
    with open("static/basic.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/demae")
def demae():
    with open("static/demae.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/book")
def book():
    with open("static/book.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/bing")
def bing():
    with open("static/bing.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/pdf")
def pdf():
    with open("static/pdf.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/long")
def long():
    with open("static/long.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/survey")
def survey():
    with open("static/survey.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/emb")
def emb():
    with open("static/emb.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/inject")
def emb():
    with open("static/inject.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/auto")
def emb():
    with open("static/auto.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# staticディレクトリにindex.htmlを置く
app.mount("/", StaticFiles(directory="static", html=True), name="static")
