from fastapi import FastAPI
from app.database import engine, Base
from app.routers import memes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(memes.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
