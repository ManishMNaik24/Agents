from tools.registry import tool_registery
from tools.retry import execute_with_retry
from tools.validator import args_validator
from tools.executor import is_duplicate_tool_call, tool_executor
import json

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


async def run_tool(tool_call,completed_tool_calls):
    
    tool_name=tool_call.function.name
    tool_args=tool_call.function.arguments
    
    if tool_name in tool_registery:
        try:
            args=json.loads(tool_args)
    
        except json.JSONDecodeError:
            tool_res={
                "ok" : False,
                "error" : {
                    "code" : "INVALID_JSON",
                    "message": "Tool arguments must be valid JSON."
                }
            }
        else :
            if isinstance(args,dict):
                args_valid=args_validator(args,tool_registery[tool_name]["schema"])
                
                if not args_valid["ok"]:
                    tool_res=args_valid
                else:
                    if not is_duplicate_tool_call(tool_name,args,completed_tool_calls):
                        tool_res=await tool_executor(tool_name,args)
                                                
                    else:
                        tool_res={
                            "ok" : False,
                            "error" : {
                                "code" : "DUPLICATE_TOOL_CALL",
                                "message" : "Tool call is repeated"
                            }
                        }
    
            else :
                tool_res={
                    "ok" : False,
                    "error" : {
                        "code" : "INVALID_DATA_FORMAT",
                        "message" : "expected dictionary"
                    }
                }
    
    else :
        tool_res = {
            "ok": False,
            "error": {
                "code": "UNKNOWN_TOOL",
                "message": f"Tool '{tool_name}' is not available."
            }
        }

    return tool_res