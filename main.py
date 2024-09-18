from flask import Flask, request, jsonify
import os
from sympy import symbols, tan, sec, sin, cot, csc, cos, integrate, sympify, log, exp

app = Flask(__name__)
def replace_and_remove(s):
    # Convert the SymPy expression to a string
    s = str(s)
    # Replace "**" with "^"
    s = s.replace("**", "^")
    # Remove all remaining "*"
    s = s.replace("*", "")
    return s

def integrate_expr(expr_str):
    # Create a local namespace with sympy functions
    local_dict = {
        'tan': tan,
        'sec': sec,
        'sin': sin,
        'cos': cos,
        'log': log,
        'exp': exp,
        'cot': cot,
        'csc': csc
    }
    
    # Convert the string to a sympy expression
    expr = sympify(expr_str, locals=local_dict)
    
    # Determine the variables in expr
    variables = expr.free_symbols
    if len(variables) == 1:
        var = variables.pop()  # Get the variable
    else:
        raise ValueError("Expression must contain exactly one variable")
    
    # Perform the integration
    integral_result = replace_and_remove(integrate(expr, var))
    return f"{integral_result} + C"

@app.route('/integrate', methods=['GET'])
def integrate_api():
    expr_str = request.args.get('expression', '')
    if not expr_str:
        return jsonify({'error': 'No expression provided'}), 400
    try:
        result = integrate_expr(expr_str)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000)
