from app.tools.registry import tool_registery
from app.tools.retry import execute_with_retry


async def tool_executor(tool_name,tool_args):
    tool=tool_registery[tool_name]["function"]
    return await execute_with_retry(tool,tool_args)


def is_duplicate_tool_call(tool_name,tool_args,completed_tool_calls):
    tool_obj={
        "tool_name" : tool_name,
        "tool_args" : tool_args
    }

    if tool_obj in completed_tool_calls:
        return True

    completed_tool_calls.append(tool_obj)
    return False
