import re

from package.tools.utils._gensim import deaccent


def make_slug(*args) -> str:
    args = list(filter(lambda x: x is not None, args))
    args = list(map(str, args))
    _id = " ".join(args)
    _id = deaccent(_id)
    _id = re.sub(r"_|[^\s\w]", " ", _id)
    _id = re.sub(r"\s+", " ", _id)
    _id = _id.strip()
    _id = re.sub(r"\s", "-", _id)
    # Change alpha -> a, beta -> b, gamma -> g, ...
    german_alphabet = {
        "ß": "ss",
    }
    for k, v in german_alphabet.items():
        _id = _id.replace(k, v)
    return _id.lower().strip()
