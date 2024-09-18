from flask import Flask, request, jsonify
from sympy import symbols, tan, sec, sin, cot, csc, cos, integrate, sympify, log, exp, pi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def replace_and_remove(s):
    # Convert the SymPy expression to a string
    s = str(s)
    # Replace "**" with "^"
    s = s.replace("**", "^")
    # Remove all remaining "*"
    s = s.replace("*", "")

    s.replace("log", "ln")

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
        'csc': csc,
        'π': pi
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


def integrate_exprs(expr_str, lower, upper):
    # Create a local namespace with sympy functions
    local_dict = {
        'tan': tan,
        'sec': sec,
        'sin': sin,
        'cos': cos,
        'log': log,
        'exp': exp,
        'cot': cot,
        'csc': csc,
        'π': pi
    }
    
    # Convert the string to a sympy expression
    expr = sympify(expr_str, locals=local_dict)
    lower = sympify(lower, locals=local_dict)
    upper = sympify(upper, locals=local_dict)
    
    # Determine the variables in expr
    variables = expr.free_symbols
    if len(variables) == 1:
        var = variables.pop()  # Get the variable
    else:
        raise ValueError("Expression must contain exactly one variable")
    
    # Perform the integration
    integral_result = replace_and_remove(integrate(expr, (var, lower, upper)))
    return f"{integral_result}"

@app.route('/integrate', methods=['GET'])
def integrate_api():
    expr_str = request.args.get('expression', '')
    isDefinite = request.args.get('definite', 'false').lower() == 'true'
    if not expr_str:
        return jsonify({'error': 'No expression provided'}), 400
    try:
        print(isDefinite)
        result = ""
        if isDefinite:
            lower = request.args.get('Lower', None)
            upper = request.args.get('Upper', None)
            if lower is None or upper is None:
                return jsonify({'error': 'Definite integration requires both Lower and Upper parameters'}), 400
            result = integrate_exprs(expr_str, lower, upper)
            return jsonify({'result': result})
        else:
            result = integrate_expr(expr_str)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
