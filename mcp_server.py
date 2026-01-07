from fastmcp import FastMCP

mcp = FastMCP("example")

@mcp.tool
def say_hello(name: str) -> str:
    return f"Ciao {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3333)
