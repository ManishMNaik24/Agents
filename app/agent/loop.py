import json
import asyncio

from llm.client import client
from llm.config import MODEL
from tools.registry import tool_registery
from tools.executor import run_tool
from prompts.system import system_prompt

messages = []

messages.append({
    "role":"system",
    "content" : system_prompt
})

available_tools=[]

for tool in tool_registery.values():
    available_tools.append(tool["schema"])

async def agent_loop():
    while True:
        user_input=input(">>")

        messages.append(
            {
                "role" : "user",
                "content" : user_input
            }
        )

        if user_input.lower() == "exit":
            break

        iteration=10

        while iteration: # tool execution loop
            iteration-=1

            response=client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=available_tools,
                temperature=0.4
            )

            assistant_response=response.choices[0].message
            # print(assistant_response)

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

                tools=[]
                completed_tool_calls=[]

                for tool_call in assistant_response.tool_calls:

                    tools.append(run_tool(tool_call,completed_tool_calls))

                results = await asyncio.gather(*tools)

                for tool_call, result in zip(assistant_response.tool_calls, results):
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(result),
                        "tool_call_id": tool_call.id
                    })

                if iteration == 0:
                    print("LLM >> Maximum agent iterations reached.")

            else:
                print(f"LLM >> {assistant_response.content}")

                messages.append({
                    "role" : "assistant",
                    "content" : assistant_response.content
                })

                break
