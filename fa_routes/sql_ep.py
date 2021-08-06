from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel

import helper
from config import logger

sql_ep = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None


@sql_ep.post('/query', tags=["run_sql"],)
async def run_query(
        request: Request,
        # item: Item,
        # sql: str = Body(...)
):
    data = await request.json()
    sql = data.get("sql")

    if (sql is not None) and (isinstance(sql, str)):
        if (
                sql.upper().startswith("INSERT") |
                sql.upper().startswith("UPDATE") |
                sql.upper().startswith("DELETE") |
                sql.upper().startswith("GRANT") |
                (not sql)
        ):
            r_msg = {
                "code": 400,
                "result": "Only SELECT statement is allowed."
            }
            raise HTTPException(status_code=400, detail=r_msg["result"])
        else:
            df = helper.run_sql(sql)
            data_rows = df.values.tolist()
            data_cols = df.columns.tolist()
            r = {
                "code": 200,
                "data": data_rows,
                "columns": data_cols
            }
            logger.info(f"SQL run successfully.")
            return r
    else:
        logger.error(f"SQL is string.")
        raise HTTPException(status_code=400)


