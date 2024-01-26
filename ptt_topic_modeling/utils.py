import unicodedata
import re
import string


def full_to_half(text):
    '''
    Transform Characters from full to half (Chinese input)
    Parameters
    ----------
    text : str
        Input string to be transform

    Returns
    -------
    string
    '''
    return ''.join([unicodedata.normalize('NFKC', char) for char in text])


def remove_html(text):
    '''

    Parameters
    ----------

    Returns
    -------
    '''
    return re.sub(r'http://\S+|https://\S+', '', text)


def strip_multi_spaces(text):
    '''

    Parameters
    ----------

    Returns
    -------
    '''
    return re.sub(r"(\s)+", " ", text)


def strip_punctuation(text):
    '''

    Parameters
    ----------

    Returns
    -------
    '''
    return re.sub(r'([%s])+' % re.escape(string.punctuation), ' ', text)
