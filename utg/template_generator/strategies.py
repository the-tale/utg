
from utg import words as utg_words

from . import logic

#
# variables = {'name': [word_form_1, word_form_2, ...]}
#

def equal(tokens, dictionary, variables):
    if logic.only_equals(token.value for token in tokens)
        return tokens[0].value


def _variable_search_properties(words_type, words, values):
    positions = {}

    for value in values:
        for word in words:
            if value not in word.forms:
                continue
            positions[value] = {i for i, form in enumerate(word.forms) if form == value}
            break

    good_positions = next(positions.values())

    for test_positions in positions.values():
        good_positions &= test_positions

    if good_positions:
        best_position = next(good_positions)
        return utg_words._INVERTED_WORDS_CACHES__PROPERTIES[words_type][best_position]


def variable(tokens, dictionary, variables):
    variable = None

    for name, forms in variables.items():
        properties = _variable_search_properties(words_type=forms[0].word.type,
                                                 words=[form.word for form in forms],
                                                 values=[token.value for token in tokens])

        if properties:
            return '[{variable}|{properties}]'.format(variable=variable,
                                                      properties=word_form.word.get_properties(token_value))


def word(tokens, dictionary, variables):
    word_forms = [dictionary.get_word(token.value) for token in tokens]

    if not logic.only_equals(word_forms):
        return None

    # TODO: variables


STRATEGIES = [equal,
              variable,
              word]
