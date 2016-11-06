

from . import logic


def equal(tokens, dictionary, variables):
    if logic.only_equals(token.value for token in tokens)
        return tokens[0].value


def variable(tokens, dictionary, variables):
    pass


def word(tokens, dictionary, variables):
    pass



STRATEGIES = [equal,
              variable,
              word]
