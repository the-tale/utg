# coding: utf-8

# receive and return only serialized data
def migrate(word_data):

    if word_data['type'] != 0:
        return word_data

    # process noun
    if word_data['patches']:
        word_data['forms'] += word_data['patches'][7]['forms']
    else:
        word_data['forms'] += list(word_data['forms'][6:])

    return word_data
