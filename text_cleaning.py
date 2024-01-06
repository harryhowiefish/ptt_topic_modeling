import re
from utils import *
from gensim.parsing.preprocessing import strip_punctuation,strip_multiple_whitespaces


def remove_html(text):
    text = re.sub('http://\S+|https://\S+', '', text)
    return text

def run_all(text):
    text = remove_html(text)
    text = full_to_half(text)
    text = strip_punctuation(text)
    text = strip_multiple_whitespaces(text)
    return text
def main():
    return
if __name__ =='__main__':
    main()