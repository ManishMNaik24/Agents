import os
import asyncio
from dotenv import load_dotenv
from db.session import SessionLocal
load_dotenv()

async def execute_attempt(tool, tool_args):
    db = None
    try:
        db = SessionLocal()

        tool_res = await asyncio.wait_for(
            tool(**tool_args, db=db),
            timeout=5
        )

        return tool_res

    except asyncio.TimeoutError:
        return {
            "ok": False,
            "error": {
                "code": "TIMEOUT_ERROR",
                "message": "Tool execution timed out."
            }
        }

    finally:
        if db:
            db.close()

async def execute_with_retry(tool, tool_args):
    tool_res=await execute_attempt(tool,tool_args)

    if tool_res["ok"]:
        return tool_res

    retry=3
    delay=1
    retryable_errors={
        "DATABASE_ERROR",
        "TIMEOUT_ERROR"
    }
    if tool_res["error"]["code"] in retryable_errors:
        while not tool_res["ok"] and tool_res["error"]["code"] in retryable_errors and retry>0:
            retry-=1
            await asyncio.sleep(delay)
            delay*=2
            tool_res=await execute_attempt(tool,tool_args)

    return tool_res
        
