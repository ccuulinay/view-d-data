from typing import Optional, Any

from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel

import helper
from config import logger

auth_ep = APIRouter()


class Cred(BaseModel):
    username: str
    password: Any


@auth_ep.post("/login", tags=["login"])
def login(cred: Cred):
    u = cred.username
    p = cred.password
    if (u is not None) and (p is not None):
        is_auth = helper.authenticate(u, p)
        if is_auth:
            r_msg = {
                "status_code": 200,
                "result": f"Welcome {u}"
            }
            return r_msg

        else:
            r_msg = {
                "code": 401,
                "result": "Please confirm your username/password and you have proper access to the tool."
            }
            raise HTTPException(status_code=401, detail=r_msg["result"])

    else:
        raise HTTPException(status_code=400)