import sys

import crawler
import text_cleaning
from tqdm import tqdm as tqdm
from utils import *
from ckiptagger import data_utils, WS, POS
from gensim.parsing.preprocessing import strip_punctuation,strip_multiple_whitespaces
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def main():
    try:
        links = crawler.crawl_links(sys.argv[1],target_num=int(sys.argv[2]))
    except IndexError:
        sys.exit("Too few arguements")
    
    posts = []
    for link in tqdm(links.values()):
        try:
            text = crawler.crawl_post(link)
            text = text_cleaning.run_all(text)
            posts.append(text)
        except:
            print(f'some error happened at when crawling {link}')
    
    print('Working on word separation....')
    ws = WS("./data")
    posts = ws(posts)
    
    print('Working on Count Vectorization....')
    cv = CountVectorizer(max_df=0.7, min_df=0.05)
    posts = [' '.join(post) for post in posts]
    matrix = cv.fit_transform(posts)
    
    print('Creating LDA....')
    LDA = LatentDirichletAllocation(n_components=5)
    LDA.fit(matrix)
    for index,topic in enumerate(LDA.components_):
        print(f'TOPIC #{index+1} 前30名詞彙')
        print([cv.get_feature_names_out()[i] for i in topic.argsort()[-30:]])
        print('\n')




if __name__ == "__main__":
    main()