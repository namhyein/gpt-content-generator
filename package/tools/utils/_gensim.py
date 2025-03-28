import unicodedata


def deaccent(text):
    """Remove letter accents from the given string.

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    str
        Unicode string without accents.

    Examples
    --------
    .. sourcecode:: pycon

        >>> from gensim.utils import deaccent
        >>> deaccent("Šéf chomutovských komunistů dostal poštou bílý prášek")
        u'Sef chomutovskych komunistu dostal postou bily prasek'

    """
    if not isinstance(text, str):
        # assume utf8 for byte strings, use default (strict) error handling
        text = text.decode("utf8")
    norm = unicodedata.normalize("NFD", text)
    result = "".join(ch for ch in norm if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", result)
