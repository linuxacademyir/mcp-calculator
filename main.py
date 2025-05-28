from fastmcp.server import FastMCP

# Define calculator tools as functions with type annotations
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Division by zero.")
    return a / b

# Create the MCP server and register tools
server = FastMCP(name="Calculator MCP Server", instructions="A remote calculator MCP server.")
server.add_tool(add, name="add", description="Add two numbers.")
server.add_tool(subtract, name="subtract", description="Subtract two numbers.")
server.add_tool(multiply, name="multiply", description="Multiply two numbers.")
server.add_tool(divide, name="divide", description="Divide two numbers.")

if __name__ == "__main__":
    server.run(transport="streamable-http", host="0.0.0.0", port=8000)
