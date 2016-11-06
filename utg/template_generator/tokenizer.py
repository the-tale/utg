from . import relations


class Token(object):
    TYPE = None
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def append(self, value):
        raise NotImplementedError

    def complete(self):
        pass

    def __hash__(self):
        return hash((self.__class__, self.value))


class Start(Token):
    TYPE = relations.TOKEN_TYPE.START


class Finish(Token):
    TYPE = relations.TOKEN_TYPE.FINISH


class Word(Token):
    TYPE = relations.TOKEN_TYPE.WORD

    def append(self, value):
        if not value.isalpha():
            return False

        self.value += value
        return True


class Number(Token):
    TYPE = relations.TOKEN_TYPE.NUMBER

    def append(self, value):
        if not value.isdigit():
            return False
        self.value += value
        return True


    def complete(self):
        self.value = int(self.value)


class Punctuation(Token):
    TYPE = relations.TOKEN_TYPE.PUNCTUATION

    def append(self, value):
        return False


class Space(Token):
    TYPE = relations.TOKEN_TYPE.SPACE

    def append(self, value):
        return False


def new_token(c):
    if c.isalpha():
        return Word(c)

    if c.isdigit():
        return Number(c)

    if c.isspace():
        return Space(c)

    return Punctuation(c)


def tokenize(text):
    token = Start()

    for c in text:
        if not token.append(c):
            yield token
            token = new_token(c)

    yield token

    yield Finish()
