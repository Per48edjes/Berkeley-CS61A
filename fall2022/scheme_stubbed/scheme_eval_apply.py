import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # BEGIN Problem 1/2
    if expr is None:
        raise SchemeError("Cannot evaluate undefined.")
    if env is None:
        raise SchemeError("No environment to evaluate expression.")

    # Evaluate atomic expressions
    if self_evaluating(expr):
        return expr
    if scheme_symbolp(expr):
        return env.lookup(expr)

    # Everything else is a Scheme list
    if not scheme_listp(expr):
        raise SchemeError(f"malformed list: {str(expr)}")

    first, rest = expr.first, expr.rest

    # Evaluate special forms
    if first == "if":
        return scheme_forms.do_if_form(rest, env)
    elif first == "lambda":
        return scheme_forms.do_lambda_form(rest, env)
    elif first == "define":
        return scheme_forms.do_define_form(rest, env)
    elif first == "quote":
        return scheme_forms.do_quote_form(rest, env)

    # Evaluate call expression
    else:
        procedure = scheme_eval(first, env)
        validate_procedure(procedure)
        args = rest.map(lambda operand: scheme_eval(operand, env))
        return scheme_apply(procedure, args, env)
    # END Problem 1/2


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    # BEGIN Problem 1/2
    # Base case: builtins don't require new environment
    python_args = args.simple_scheme_to_python_list()
    if procedure.need_env:
        python_args.append(env)
    try:
        return procedure.py_func(*python_args)
    except TypeError:
        raise SchemeError("incorrect number of arguments")
    # END Problem 1/2


##################
# Tail Recursion #
##################

# Make classes/functions for creating tail recursive programs here!
# BEGIN Problem EC
"*** YOUR CODE HERE ***"
# END Problem EC


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    validate_procedure(procedure)
    # BEGIN
    return val
    # END
