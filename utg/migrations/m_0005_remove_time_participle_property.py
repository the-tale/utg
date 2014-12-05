# coding: utf-8

# receive and return only serialized data
def migrate(word_data):

    if word_data['type'] != 4:
        return word_data

    if '5' in word_data['properties']:
        del word_data['properties']['5']

    return word_data
