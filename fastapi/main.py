from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import simple,order

app = FastAPI()

# /simple
app.include_router(simple.router)

# /order
app.include_router(order.router)

# staticディレクトリにindex.htmlを置く
app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.mount("/demae", StaticFiles(directory="static", html=True), name="static")