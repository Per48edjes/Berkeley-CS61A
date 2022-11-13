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
    pass


def do_quote_form(rest, env):
    return rest.first


def do_define_form(rest, env):
    symbol, value = rest.first, scheme_eval(rest.rest.first, env)
    if not scheme_symbolp(symbol):
        raise SchemeError("invalid symbol: {symbol}")
    env.define(symbol, value)
    return symbol


# END PROBLEM 1/2/3
