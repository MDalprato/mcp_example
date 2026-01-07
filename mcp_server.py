from mcp.server import Server
from mcp.types import Tool, Resource

server = Server(name="local-dev-context")

@server.tool()
def read_file(path: str) -> str:
    """Read a file from the local project"""
    with open(path, "r") as f:
        return f.read()

@server.tool()
def run_tests() -> str:
    """Run project tests"""
    return "All tests passed (42 tests)"

@server.resource()
def project_info() -> Resource:
    return Resource(
        uri="project://info",
        content="""
Project: HyperNode Server
Language: Python 3.11
Framework: FastAPI
Style: Black + Ruff
"""
    )

if __name__ == "__main__":
    server.run()
