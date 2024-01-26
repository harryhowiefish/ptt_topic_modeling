import json
from tqdm import tqdm as tqdm
from ckiptagger import WS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from datetime import datetime
import ptt_topic_modeling.utils as utils
import ptt_topic_modeling.crawler as crawler


def board_to_post(board, num):
    links = crawler.crawl_links(board, target_num=num)
    posts = []
    for link in tqdm(links.values()):
        text = crawler.crawl_post(link)
        if text is None:
            print(f'fail to crawl the following page: {link}')
            return
        text = utils.remove_html(text)
        text = utils.full_to_half(text)
        text = utils.strip_punctuation(text)
        text = utils.strip_multiple_whitespaces(text)
        posts.append(text)
    return posts


def posts_to_topic(posts):

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
    result = {}

    for index, topic in enumerate(LDA.components_):
        result[f'topic_{index+1}'] = [
            cv.get_feature_names_out()[i] for i in topic.argsort()[-30:]]
    result['create_time'] = str(datetime.now())
    return result


def to_json(d, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False)
