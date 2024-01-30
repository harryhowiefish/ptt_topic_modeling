import unicodedata
import re
import string
import json


def full_to_half(text: str) -> str:
    '''
    Transform Characters from full to half. (Chinese input)

    Parameters
    ----------
    text : str
        Input string to be transform

    Returns
    -------
    string
    '''
    return ''.join([unicodedata.normalize('NFKC', char) for char in text])


def remove_html(text: str) -> str:
    '''
    Parse and remove html/htmls from text.

    Parameters
    ----------
    text : str
        Input string to be transform

    Returns
    -------
    string
    '''
    return re.sub(r'http://\S+|https://\S+', '', text)


def strip_multi_spaces(text: str) -> str:
    '''
    Remove multiple whitespaces.
    This can be caused by user input and
    strip_punctuation function.

    Parameters
    ----------
    text : str
        Input string to be transform

    Returns
    -------
    string
    '''
    return re.sub(r"(\s)+", " ", text)


def strip_punctuation(text: str) -> str:
    '''
    Remove all punctuation, replace with whitespace

    Parameters
    ----------
    text : str
        Input string to be transform

    Returns
    -------
    string
    '''
    return re.sub(r'([%s])+' % re.escape(string.punctuation), ' ', text)


def to_json(_dict: dict, path: str) -> None:
    '''
    Save the resulting dictionary (keyword and date)
    as json.

    Parameters
    ----------
    _dict : dict
        Input string to be transform
    path : str
        Path for json file

    Returns
    -------
    None
    '''
    with open(path, 'w', encoding='utf8') as f:
        json.dump(_dict, f, ensure_ascii=False)
