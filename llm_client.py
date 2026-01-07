from openai import OpenAI

def say_hello(name: str) -> str:
    return f"Ciao {name}!"

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Saluta Marco",
    tools=[{
        "type": "function",
        "function": {
            "name": "say_hello",
            "description": "Saluta una persona",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": { "type": "string" }
                },
                "required": ["name"]
            }
        }
    }]
)

# se il modello chiama il tool
for item in response.output:
    if item["type"] == "tool_call":
        print(say_hello(**item["arguments"]))
