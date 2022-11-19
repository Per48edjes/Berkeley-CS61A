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
    if is_scheme_true(scheme_eval(predicate, env)):
        return scheme_eval(consequent, env, True)
    return scheme_eval(alternative, env, True)


def do_cond_form(rest, env):
    if rest is nil:
        return env.lookup("undefined")
    predicate, subexpression = rest.first.first, rest.first.rest
    predicate_value = (
        True
        if predicate == "else" and rest.rest is nil
        else scheme_eval(predicate, env)
    )
    if is_scheme_true(predicate_value):
        return (
            do_begin_form(subexpression, env)
            if subexpression is not nil
            else predicate_value
        )
    return do_cond_form(rest.rest, env)


def do_and_form(rest, env):
    if rest is nil:
        return True
    test_value = scheme_eval(rest.first, env, True) if rest.rest is nil else scheme_eval(rest.first, env)
    if is_scheme_true(test_value) and rest.rest is not nil:
        return do_and_form(rest.rest, env)
    else:
        return test_value


def do_or_form(rest, env):
    if rest is nil:
        return False
    test_value = scheme_eval(rest.first, env, True) if rest.rest is nil else scheme_eval(rest.first, env)
    if is_scheme_false(test_value) and rest.rest is not nil:
        return do_or_form(rest.rest, env)
    else:
        return test_value


def do_lambda_form(rest, env):
    if rest.rest is nil:
        raise SchemeError("Lambda expression requires a body!")
    return LambdaProcedure(rest.first, rest.rest, env)


def do_mu_form(rest, env):
    if rest.rest is nil:
        raise SchemeError("Mu expression requires a body!")
    return MuProcedure(rest.first, rest.rest)


def do_quote_form(rest, env):
    return rest.first


def do_begin_form(rest, env):
    evaluated_subexpression = None
    while rest is not nil:
        subexpression, rest = rest.first, rest.rest
        evaluated_subexpression = scheme_eval(subexpression, env, True) if rest is nil else scheme_eval(subexpression, env)
    return evaluated_subexpression


def do_let_form(rest, env):
    let_frame = Frame(env)
    bindings, body = rest.first, rest.rest
    while bindings is not nil:
        binding = bindings.first
        validate_form(binding, 2, 2)
        if scheme_symbolp(binding.first):
            symbol, value = binding.first, scheme_eval(binding.rest.first, env)
            let_frame.define(symbol, value)
        else:
            raise SchemeError(f"Invalid symbol!")
        bindings = bindings.rest
    return do_begin_form(body, let_frame)


def do_define_form(rest, env):
    if scheme_listp(rest.first):
        symbol, formals, body = rest.first.first, rest.first.rest, rest.rest
        validate_formals(formals)
        value = LambdaProcedure(formals, body, env)
    elif scheme_symbolp(rest.first):
        symbol, value = rest.first, scheme_eval(rest.rest.first, env)
    else:
        raise SchemeError(f"Invalid symbol!")
    env.define(symbol, value)
    return symbol


# END PROBLEM 1/2/3
