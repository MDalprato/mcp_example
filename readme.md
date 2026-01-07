# MCP Example

Minimal MCP server/client example in Python.

## Setup

```sh
cd mcp_example
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install mcp openai
```

## Run

```sh
python3 mcp_server.py
```

```sh
export OPENAI_API_KEY="your_key_here"
python3 client.py
```
