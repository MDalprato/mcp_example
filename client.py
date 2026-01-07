from mcp.client import MCPClient
from openai import OpenAI

mcp = MCPClient("http://localhost:3333")
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Why are my tests slow?",
    tools=mcp.tools(),
    resources=mcp.resources()
)

print(response.output_text)
