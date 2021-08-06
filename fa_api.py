import uvicorn
from fastapi import FastAPI, Request, HTTPException

import os
import sys
import pathlib
import joblib
import logging
import random

import helper
from config import logger
from fa_routes import sql_ep, auth_ep

APP_NAME = "VIEW_D_DATA_FA_API"

app = FastAPI(title=APP_NAME, description="API for View D Data", version="1.0")


@app.on_event('startup')
def load_db_connection():
    helper.connect_db()


@app.get("/ping")
def pong():
    pop = ["pong", "oop!"]
    r = random.choices(population=pop, weights=[0.8, 0.2], k=1)
    return r[0]


app.include_router(sql_ep.sql_ep, prefix='/v1')
app.include_router(auth_ep.auth_ep)

# 4. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=10087)

