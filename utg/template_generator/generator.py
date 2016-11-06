
from . import logic
from . import tokenizer
from . import exceptions
from . import strategies



def generate(texts, dictionary, variables):

    tokenized_texts = []

    for text in texts:
        tokenized_texts.append([token for token in tokenizer.tokenize(text) if not token.type.is_SPACE])

    if not logic.only_equals(len(tokens) for tokens in tokenized_texts):
        raise DifferentRawTextsTokensNumber()

    for tokens in zip(*tokenized_texts):
        if not logic.only_equals(token.type for token in tokens):
            raise DifferentTokenTypesTakeOnePlace()

    template_source = []

    for tokens in zip(*tokenized_texts):
        for strategy in strategies.STRATEGIES:
            result = strategy.apply(tokens, dictionary, variables):
            if result:
                template_source.append(result)
                break

    return finish_template(template_source)


def finish_template(template_source):
    return ' '.join(template_source)
