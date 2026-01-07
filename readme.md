# MCP Example

A minimal Python example of an MCP server and client.

## Requirements

- Python 3.10+

## Setup

```sh
cd mcp_example
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install mcp openai
```

## Run the server

```sh
python3 mcp_server.py
```

## Test the endpoint

```sh
curl -X POST http://127.0.0.1:3333/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "list_tools"
  }'
```
