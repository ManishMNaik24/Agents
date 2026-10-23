import asyncio

from db.session import SessionLocal


async def execute_with_retry(tool, tool_args):
    db=SessionLocal()
    try:
        tool_res=tool(**tool_args,db=db)
    finally:
        db.close()

    if tool_res["ok"]:
        return tool_res

    if tool_res["error"]["code"] == "DATABASE_ERROR":
        retries=3
        delay=1

        while not tool_res["ok"] and tool_res["error"]["code"] == "DATABASE_ERROR" and retries > 0:
            retries-=1
            await asyncio.sleep(delay) # delay is required because retrying immediately often means you hit the same temporary failure again.
            delay *= 2
            db=SessionLocal()
            try:
                tool_res=tool(**tool_args,db=db)
            finally:
                db.close()

    return tool_res
