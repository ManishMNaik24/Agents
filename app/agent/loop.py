import json

from app.llm.client import client
from app.llm.config import MODEL
from app.tools.executor import is_duplicate_tool_call, tool_executor
from app.tools.registry import tool_registery
from app.tools.validator import args_validator


messages = []

messages.append({
    "role":"system",
    "content" : "You are a helpful AI assistant and "
    "your task is to answer questions without hallucinations."
})

available_tools=[]

for tool in tool_registery.values():
    available_tools.append(tool["schema"])

async def agent_loop():
    while True:
        user_input=input(">>")
        print(f">> {user_input}")

        messages.append(
            {
                "role" : "user",
                "content" : user_input
            }
        )

        if user_input.lower() == "exit":
            break


        response=client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=available_tools
        )

        assistant_response=response.choices[0].message

        if assistant_response.tool_calls:
            tool_call_list=[]
            for tool_call in assistant_response.tool_calls:
                tool_name=tool_call.function.name
                tool_args=tool_call.function.arguments

                tool_call_list.append({
                    "id" : tool_call.id,
                    "type" : "function",
                    "function" : {
                        "name" : tool_name,
                        "arguments" : tool_args
                    }
                })

            messages.append({
                "role":"assistant",
                "content" : None,
                "tool_calls" : tool_call_list
            })

            completed_tool_calls=[]

            for tool_call in assistant_response.tool_calls:

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

                messages.append({
                    "role" : "tool",
                    "content" : json.dumps(tool_res),
                    "tool_call_id" : tool_call.id
                })

        else:
            print(f"LLM >> {assistant_response.content}")

            messages.append({
                "role" : "assistant",
                "content" : assistant_response.content
            })
