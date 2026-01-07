from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI

client = OpenAI()

# === TOOL ===
def say_hello(name: str) -> str:
    return f"Ciao {name}!"

tools = [
    {
        "type": "function",
        "name": "say_hello",
        "description": "Say hi to a person",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
    }
]

# === STEP 1: MODEL DECIDES ===
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hi to Marco",
    tools=tools
)

tool_output = None

for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        tool_output = say_hello(**args)

# === STEP 2: MODEL REACTS TO TOOL RESULT ===
final = client.responses.create(
    model="gpt-4.1-mini",
    input=f"The tool returned this result: {tool_output}. Respond politely to the user."
)

print(final.output_text)
