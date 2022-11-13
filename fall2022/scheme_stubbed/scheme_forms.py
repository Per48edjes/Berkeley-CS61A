from scheme_builtins import *
from scheme_classes import *
from scheme_eval_apply import *
from scheme_utils import *

#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

# BEGIN PROBLEM 1/2/3
def do_if_form(rest, env):
    predicate, consequent, alternative = (
        rest.first,
        rest.rest.first,
        rest.rest.rest.first,
    )
    if scheme_eval(predicate, env):
        return scheme_eval(consequent, env)
    return scheme_eval(alternative, env)


def do_lambda_form(rest, env):
    if rest.rest is nil:
        raise SchemeError("Lambda expression requires a body!")
    return LambdaProcedure(rest.first, rest.rest, env)


def do_quote_form(rest, env):
    return rest.first


def do_begin_form(rest, env):
    evaluated_subexpression = None
    while rest is not nil:
        subexpression = rest.first
        evaluated_subexpression = scheme_eval(subexpression, env)
        rest = rest.rest
    return evaluated_subexpression


def do_define_form(rest, env):
    if scheme_listp(rest.first):
        symbol, formals, body = rest.first.first, rest.first.rest, rest.rest
        value = LambdaProcedure(formals, body, env)
    elif scheme_symbolp(rest.first):
        symbol, value = rest.first, scheme_eval(rest.rest.first, env)
    else:
        raise SchemeError(f"invalid symbol: {symbol}")
    env.define(symbol, value)
    return symbol


# END PROBLEM 1/2/3
