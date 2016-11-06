
from utg import exceptions


class TemplateGeneratorError(exceptions.UtgError):
    MSG = 'template generator error'


class DifferentRawTextsTokensNumber(TemplateGeneratorError):
    MSG = 'raw texts has different tokens number'


class DifferentTokenTypesTakeOnePlace(TemplateGeneratorError):
    MGS = 'different token types take on place in raw texts'
