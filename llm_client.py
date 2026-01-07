from dotenv import load_dotenv

load_dotenv()

import json
from openai import OpenAI

client = OpenAI()


# === TOOL ===
def say_hello(name: str) -> str:
    return f"Ciao {name}!"


def somma(a: float, b: float) -> float:
    return a + b


tools = [
    {
        "type": "function",
        "name": "say_hello",
        "description": "Say hi to a person",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "sum",
        "description": "Sum two numbers",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        },
    },
]

# === STEP 1: MODEL DECIDES ===
# response = client.responses.create(
#     model="gpt-4.1-mini", input="Say hi to Marco", tools=tools
# )

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Quanto fa 12.5 + 7.3?",
    tools=tools
)


tool_output = None


for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        result = somma(**args)
        
        tool_output = result
        

# for item in response.output:
#     if item.type == "function_call":
#         args = json.loads(item.arguments)
#         tool_output = say_hello(**args)

# === STEP 2: MODEL REACTS TO TOOL RESULT ===
final = client.responses.create(
    model="gpt-4.1-mini",
    input=f"The tool returned this result: {tool_output}. Respond politely to the user with the result as a lenght measure (meters)",
)


print(final.output_text)


