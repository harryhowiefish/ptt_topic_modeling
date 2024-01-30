from ckiptagger import WS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from datetime import datetime
import logging
from typing import List


# this can be further broken down to posts_to_matrix
# matrix_to_lda
# lda_extract_topics
def posts_to_topic(posts: List[str],
                   topic_num: int = 5,
                   top_word: int = 30) -> dict:
    '''
    Use the given posts to generate topics and extract key words

    Parameters
    ----------
    posts : list
        Text from ptt posts

    topic_num : int
        Number of topics to extract

    top_word : int
        Number of words per topic

    Returns
    -------
    dict
        {topics: dict, create_time: datetime string}
    '''
    if topic_num < 0:
        raise ValueError("topic_num must be non-negative integer")

    if top_word < 0:
        raise ValueError("top_word must be non-negative integer")

    logging.info('Working on word separation....')
    # catch error here
    try:
        ws = WS("./data")
        posts = ws(posts)
    except FileNotFoundError:
        raise FileNotFoundError("Can't find model. Please download Ckip model")
    except AttributeError:
        raise FileNotFoundError(
            "Please make sure model_ws is in the data folder")
    logging.info('Working on Count Vectorization....')
    cv = CountVectorizer(max_df=0.7, min_df=0.05)
    posts = [' '.join(post) for post in posts]
    matrix = cv.fit_transform(posts)

    logging.info('Creating LDA....')
    LDA = LatentDirichletAllocation(n_components=topic_num)
    LDA.fit(matrix)
    result = {'topics': {}}

    for index, topic in enumerate(LDA.components_):
        result['topics'][f'topic_{index+1}'] = [
            cv.get_feature_names_out()[i] for i in topic.argsort()[-top_word:]]
    result['create_time'] = str(datetime.now())
    return result
