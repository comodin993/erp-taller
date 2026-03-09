import unicodedata


def normalize(text):

    text = text.lower()

    text = unicodedata.normalize('NFD', text)

    text = ''.join(
        c for c in text
        if unicodedata.category(c) != 'Mn'
    )

    return text


def search(items, query):

    q = normalize(query)

    results = []

    for item in items:

        text = " ".join(str(v) for v in item.values())

        if q in normalize(text):
            results.append(item)

    return results