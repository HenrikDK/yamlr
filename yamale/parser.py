import ast

from yamale.validators import validators as val

safe_globals = ("True", "False", "None")
safe_builtins = dict((f, __builtins__[f]) for f in safe_globals)


def _extract_expression(call_node, validators):
    result = {}
    # Validate that the expression uses a known, registered validator.
    try:
        
        func_name = call_node.func.id
        
        kw_args = {} 
        for kw in call_node.keywords:
          kw_args[kw.arg] = kw.value.value
        
        args = [a.value for a in call_node.args if isinstance(a, ast.Constant)]
        result = {
            'name': func_name,
            'args': args,
            'kw_args': kw_args,
            'children': []
        }
    except AttributeError:
        raise SyntaxError("Schema expressions must be enclosed by a validator.")
    if func_name not in validators:
        raise SyntaxError("Not a registered validator: '%s'. " % func_name)
    
    # Validate that all args are constant literals, validator names, or other call nodes
    arg_values = call_node.args + [kw.value for kw in call_node.keywords]
    for arg in arg_values:
        base_arg = arg.operand if isinstance(arg, ast.UnaryOp) else arg
        if isinstance(base_arg, ast.Constant):
            continue
        elif isinstance(base_arg, ast.Name) and base_arg.id in validators:
            continue
        elif isinstance(base_arg, ast.Call):
            child = _extract_expression(base_arg, validators)
            result['children'].append(child)
        else:
            raise SyntaxError("Argument values must either be constant literals, or else " "reference other validators.")
    return result


def parse(validator_string, validators=None):
    validators = validators or val.DefaultValidators
    try:
        tree = ast.parse(validator_string, mode="eval")
        result = _extract_expression(tree.body, validators)
        return result
    except (SyntaxError, NameError, TypeError) as e:
        raise SyntaxError("Invalid schema expression: '%s'. " % validator_string + str(e))
