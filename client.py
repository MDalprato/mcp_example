from fastmcp import Client

with Client.command(["python", "mcp_server.py"]) as client:
    tools = client.list_tools()
    print("TOOLS:", tools)

    result = client.call_tool(
        "say_hello",
        {"name": "Marco"}
    )
    print("RESULT:", result)
