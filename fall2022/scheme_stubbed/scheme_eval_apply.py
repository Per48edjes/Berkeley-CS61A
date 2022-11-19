import os
import sys

import scheme_forms
from pair import *
from scheme_utils import *
from ucb import main, trace

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
    if first == "cond":
        return scheme_forms.do_cond_form(rest, env)
    if first == "and":
        return scheme_forms.do_and_form(rest, env)
    if first == "or":
        return scheme_forms.do_or_form(rest, env)
    elif first == "lambda":
        return scheme_forms.do_lambda_form(rest, env)
    elif first == "mu":
        return scheme_forms.do_mu_form(rest, env)
    elif first == "define":
        return scheme_forms.do_define_form(rest, env)
    elif first == "let":
        return scheme_forms.do_let_form(rest, env)
    elif first == "quote":
        return scheme_forms.do_quote_form(rest, env)
    elif first == "begin":
        return scheme_forms.do_begin_form(rest, env)

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
    if isinstance(procedure, BuiltinProcedure):
        python_args = args.simple_scheme_to_python_list()
        if procedure.need_env:
            python_args.append(env)
        try:
            return procedure.py_func(*python_args)
        except TypeError:
            raise SchemeError("incorrect number of arguments")
    elif isinstance(procedure, LambdaProcedure):
        function_frame = procedure.env.make_child_frame(procedure.formals, args)
    elif isinstance(procedure, MuProcedure):
        function_frame = env.make_child_frame(procedure.formals, args)
    return scheme_forms.do_begin_form(procedure.body, function_frame)
    # END Problem 1/2


##################
# Tail Recursion #
##################

# Make classes/functions for creating tail recursive programs here!
# BEGIN Problem EC
class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""

    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        result = Unevaluated(expr, env)
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return result
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env)
        return result

    return optimized_eval


# END Problem EC


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    # BEGIN
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    return val
    # END


scheme_eval = optimize_tail_calls(scheme_eval)
