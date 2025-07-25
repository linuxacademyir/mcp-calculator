import os
os.environ["FASTMCP_SERVER_HOST"] = "0.0.0.0"
os.environ["FASTMCP_SERVER_PORT"] = "8000"

from dotenv import load_dotenv
load_dotenv()

# To control host/port, set environment variables:
#   FASTMCP_SERVER_HOST=0.0.0.0 FASTMCP_SERVER_PORT=8000 python app.py

from mcp.server.fastmcp import FastMCP
import math
import numpy as np
from scipy import stats  # Importing scipy for advanced statistical functions
from sympy import symbols, solve, sympify, diff, integrate
from typing import List, Tuple
from pydantic import Field

# Create MCP Server
app = FastMCP(
    title="Mathematical Calculator",
    description="A server for complex mathematical calculations",
    version="1.0.0",
    dependencies=["numpy", "scipy", "sympy"],
    stateless_http=True,
    host="0.0.0.0",
    port=8000   
)

print("FASTMCP_SERVER_HOST:", os.environ.get("FASTMCP_SERVER_HOST"))
print("FASTMCP_SERVER_PORT:", os.environ.get("FASTMCP_SERVER_PORT"))

@app.tool()
def calculate(expression: str) -> dict:
    """
    Evaluates a mathematical expression and returns the result.

    Supports basic operators (+, -, *, /, **, %), mathematical functions
    (sin, cos, tan, exp, log, log10, sqrt), and constants (pi, e).
    Uses a restricted evaluation context for safe execution.

    Args:
        expression: The mathematical expression to evaluate as a string.
                   Examples: "2 + 2", "sin(pi/4)", "sqrt(16) * 2", "log(100, 10)"

    Returns:
        On success: {"result": <calculated value>}
        On error: {"error": <error message>}

    Examples:
        >>> calculate("2 * 3 + 4")
        {'result': 10}
        >>> calculate("sin(pi/2)")
        {'result': 1.0}
        >>> calculate("sqrt(16)")
        {'result': 4.0}
        >>> calculate("invalid * expression")
        {'error': "name 'invalid' is not defined"}
    """
    try:
        # Safe evaluation of the expression
        result = eval(expression, {"__builtins__": {}}, {
            "math": math,
            "np": np,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "exp": math.exp,
            "log": math.log,
            "log10": math.log10,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e
        })
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def solve_equation(equation: str) -> dict:
    """
    Solves an algebraic equation for x and returns all solutions.

    The equation must contain exactly one equality sign (=) and use a
    variable x. Can solve polynomial, trigonometric, and other equations
    supported by SymPy.

    Args:
        equation: The equation to solve as a string.
                 Format: '<left side> = <right side>'
                 Examples: "x**2 - 5*x + 6 = 0", "sin(x) = 0.5", "2*x + 3 = 7"

    Returns:
        On success: {"solutions": <list of solutions as string>}
        On error: {"error": <error message>}

    Examples:
        >>> solve_equation("x**2 - 5*x + 6 = 0")
        {'solutions': '[2, 3]'}
        >>> solve_equation("2*x + 3 = 7")
        {'solutions': '[2]'}
        >>> solve_equation("x = 0")
        {'solutions': '[0]'}

    Notes:
        - Use 'x' as the variable (e.g., x**2, not x²)
        - Multiplication must be explicitly indicated with * (e.g., 2*x, not 2x)
        - Powers are represented with ** (e.g., x**2, not x^2)
    """
    try:
        x = symbols('x')
        # Split the equation into left and right sides
        parts = equation.split('=')
        if len(parts) != 2:
            return {"error": "Equation must contain an '=' sign"}

        left = sympify(parts[0].strip())
        right = sympify(parts[1].strip())

        # Solve the equation
        solutions = solve(left - right, x)
        return {"solutions": str(solutions)}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def differentiate(expression: str, variable: str = "x") -> dict:
    """
    Computes the derivative of a mathematical expression with respect to a variable.

    Supports polynomials, trigonometric functions, exponential functions,
    logarithms, and other functions supported by SymPy.

    Args:
        expression: The mathematical expression to differentiate as a string.
                   Examples: "x**2", "sin(x)", "exp(x)", "log(x)"
        variable: The variable with respect to which to differentiate. Default is "x".
                 Optionally, other variables can be specified.

    Returns:
        On success: {"result": <derivative as string>}
        On error: {"error": <error message>}

    Examples:
        >>> differentiate("x**2")
        {'result': '2*x'}
        >>> differentiate("sin(x)")
        {'result': 'cos(x)'}
        >>> differentiate("x*y", "y")
        {'result': 'x'}
        >>> differentiate("exp(x)")
        {'result': 'exp(x)'}

    Notes:
        - Use mathematical notation with explicit operators (* for multiplication)
        - Powers are represented with ** (e.g., x**2, not x^2)
        - For trigonometric functions, use sin(x), cos(x), etc.
    """
    try:
        var = symbols(variable)
        expr = sympify(expression)
        result = diff(expr, var)
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}


from sympy import integrate as sympy_integrate

@app.tool()
def integrate(expression: str, variable: str = "x") -> dict:
    """
    Computes the indefinite integral of a mathematical expression with respect to a variable.

    Supports polynomials, trigonometric functions, exponential functions,
    logarithms, and other functions supported by SymPy.

    Args:
        expression: The mathematical expression to integrate as a string.
                   Examples: "x**2", "sin(x)", "exp(x)", "1/x"
        variable: The variable with respect to which to integrate. Default is "x".
                 Optionally, other variables can be specified.

    Returns:
        On success: {"result": <integral as string>}
        On error: {"error": <error message>}

    Examples:
        >>> integrate("x**2")
        {'result': 'x**3/3'}
        >>> integrate("sin(x)")
        {'result': '-cos(x)'}
        >>> integrate("exp(x)")
        {'result': 'exp(x)'}
        >>> integrate("1/x")
        {'result': 'log(x)'}
        >>> integrate("x*y", "y")
        {'result': 'x*y**2/2'}

    Notes:
        - The result is the indefinite integral without the constant of integration
        - Complex expressions may be returned in simplified form
    """
    try:
        var = symbols(variable)
        expr = sympify(expression)
        result = sympy_integrate(expr, var)  # Use sympy_integrate instead of integrate
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def mean(data: List[float]) -> dict:
    """
    Computes the mean of a list of numbers.

    Args:
        data: A list of numerical values.

    Returns:
        On success: {"result": <mean value>}
        On error: {"error": <error message>}

    Examples:
        >>> mean([1, 2, 3, 4])
        {'result': 2.5}
        >>> mean([10, 20, 30])
        {'result': 20.0}
    """
    try:
        result = float(np.mean(data))
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def variance(data: List[float]) -> dict:
    """
    Computes the variance of a list of numbers.

    Args:
        data: A list of numerical values.

    Returns:
        On success: {"result": <variance value>}
        On error: {"error": <error message>}

    Examples:
        >>> variance([1, 2, 3, 4])
        {'result': 1.25}
    """
    try:
        result = float(np.var(data))
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def standard_deviation(data: List[float]) -> dict:
    """
    Computes the standard deviation of a list of numbers.

    Args:
        data: A list of numerical values.

    Returns:
        On success: {"result": <standard deviation value>}
        On error: {"error": <error message>}

    Examples:
        >>> standard_deviation([1, 2, 3, 4])
        {'result': 1.118033988749895}
    """
    try:
        result = float(np.std(data))
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def median(data: List[float]) -> dict:
    """
    Computes the median of a list of numbers.

    Args:
        data: A list of numerical values.

    Returns:
        On success: {"result": <median value>}
        On error: {"error": <error message>}

    Examples:
        >>> median([1, 2, 3, 4])
        {'result': 2.5}
    """
    try:
        result = float(np.median(data))
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def mode(data: List[float]) -> dict:
    """
    Computes the mode of a list of numbers.

    Args:
        data: A list of numerical values.

    Returns:
        On success: {"result": <mode value>}
        On error: {"error": <error message>}

    Examples:
        >>> mode([1, 2, 2, 3])
        {'result': 2.0}
        >>> mode([1, 1, 2, 2])
        {'result': 1.0}
        >>> mode([])
        {'error': 'Cannot compute mode of empty array'}
    """
    try:
        if not data:
            return {"error": "Cannot compute mode of empty array"}
        # Adjusted for newer SciPy versions
        mode_result = stats.mode(data, keepdims=False)
        return {"result": float(mode_result.mode)}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def correlation_coefficient(data_x: List[float], data_y: List[float]) -> dict:
    """
    Computes the Pearson correlation coefficient between two lists of numbers.

    Args:
        data_x: The first list of numerical values.
        data_y: The second list of numerical values.

    Returns:
        On success: {"result": <correlation coefficient>}
        On error: {"error": <error message>}

    Examples:
        >>> correlation_coefficient([1, 2, 3], [4, 5, 6])
        {'result': 1.0}
    """
    try:
        result = np.corrcoef(data_x, data_y)[0, 1]
        return {"result": float(result)}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def linear_regression(data: List[Tuple[float, float]]) -> dict:
    """
    Performs linear regression on a set of points and returns the slope and intercept.

    Args:
        data: A list of tuples, where each tuple contains (x, y) coordinates.

    Returns:
        On success: {"slope": <slope value>, "intercept": <intercept value>}
        On error: {"error": <error message>}

    Examples:
        >>> linear_regression([(1, 2), (2, 3), (3, 5)])
        {'slope': 1.5, 'intercept': 0.3333333333333335}
    """
    try:
        x = np.array([point[0] for point in data])
        y = np.array([point[1] for point in data])
        slope, intercept, _, _, _ = stats.linregress(x, y)
        return {"slope": float(slope), "intercept": float(intercept)}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def confidence_interval(data: List[float], confidence: float = 0.95) -> dict:
    """
    Computes the confidence interval for the mean of a dataset.

    Args:
        data: A list of numerical values.
        confidence: The confidence level (default is 0.95).

    Returns:
        On success: {"confidence_interval": <(lower_bound, upper_bound)>}
        On error: {"error": <error message>}

    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)  # For reproducible results
        >>> confidence_interval([1, 2, 3, 4])
        {'confidence_interval': (0.445739743239121, 4.5542602567608785)}
    """
    try:
        mean_value = np.mean(data)
        sem = stats.sem(data)  # Standard error of the mean
        margin_of_error = sem * stats.t.ppf((1 + confidence) / 2, len(data) - 1)
        return {"confidence_interval": (float(mean_value - margin_of_error), float(mean_value + margin_of_error))}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def matrix_addition(matrix_a: List[List[float]], matrix_b: List[List[float]]) -> dict:
    """
    Adds two matrices.

    Args:
        matrix_a: The first matrix as a list of lists.
        matrix_b: The second matrix as a list of lists.

    Returns:
        On success: {"result": <resulting matrix>}
        On error: {"error": <error message>}

    Examples:
        >>> matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        {'result': [[6, 8], [10, 12]]}
    """
    try:
        result = np.add(matrix_a, matrix_b).tolist()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def matrix_multiplication(matrix_a: List[List[float]], matrix_b: List[List[float]]) -> dict:
    """
    Multiplies two matrices.

    Args:
        matrix_a: The first matrix as a list of lists.
        matrix_b: The second matrix as a list of lists.

    Returns:
        On success: {"result": <resulting matrix>}
        On error: {"error": <error message>}

    Examples:
        >>> matrix_multiplication([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        {'result': [[19, 22], [43, 50]]}
    """
    try:
        result = np.dot(matrix_a, matrix_b).tolist()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.tool()
def matrix_transpose(matrix: List[List[float]]) -> dict:
    """
    Transposes a matrix.

    Args:
        matrix: The matrix to transpose as a list of lists.

    Returns:
        On success: {"result": <transposed matrix>}
        On error: {"error": <error message>}

    Examples:
        >>> matrix_transpose([[1, 2], [3, 4]])
        {'result': [[1, 3], [2, 4]]}
    """
    try:
        result = np.transpose(matrix).tolist()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app.run(transport="sse")