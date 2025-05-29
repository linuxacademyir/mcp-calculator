from fastmcp.server import FastMCP

# Create the MCP server and register tools
server = FastMCP(
    name="Calculator MCP Server",
    instructions="A remote calculator MCP server.",
    stateless_http=True  # This disables session requirements
)

@server.tool(name="add", description="Add two numbers.")
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@server.tool(name="subtract", description="Subtract two numbers.")
def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

@server.tool(name="multiply", description="Multiply two numbers.")
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@server.tool(name="divide", description="Divide two numbers.")
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Division by zero.")
    return a / b

if __name__ == "__main__":
    server.run(transport="streamable-http", host="0.0.0.0", port=8000)
