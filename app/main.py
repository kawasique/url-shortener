from typing import Annotated

from fastapi import FastAPI, Depends
import auth


app = FastAPI()


@app.get("/", dependencies=[Depends(auth.verify_key)])
async def root():
    return {"message": "Hello, world!"}
