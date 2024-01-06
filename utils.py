import unicodedata

def replace_char(char_list, text):
    for char in char_list:
        text = text.replace(*char)
    return text

def full_to_half(text):
    return ''.join([unicodedata.normalize('NFKC', char) for char in text])