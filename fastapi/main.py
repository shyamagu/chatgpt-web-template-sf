from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import simple,order

app = FastAPI()

app.include_router(simple.router)
app.include_router(order.router)

# staticディレクトリにindex.htmlを置く
app.mount("/", StaticFiles(directory="static", html=True), name="static")