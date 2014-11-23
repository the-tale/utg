
# receive and return only serialized data
def migrate(word_data):

    if word_data['type'] != 10: # preposition
        return word_data

    word_data['forms'].append(word_data['forms'][-1])

    return word_data
