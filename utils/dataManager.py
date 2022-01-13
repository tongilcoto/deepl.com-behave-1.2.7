import json
from random import randrange


def get_random_data(original_language, topic, subtopic):

    dataBase = json.load(open(f"data/{original_language}/{topic}.json"))[subtopic]

    return dataBase[randrange(len(dataBase))]


def serialize_and_sort(item):
    if isinstance(item, dict):
        return sorted((key, serialize_and_sort(values)) for key, values in item.items())
    if isinstance(item, list):
        return sorted(serialize_and_sort(x) for x in item)
    else:
        return item
