from ckiptagger import WS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from datetime import datetime


# this can be further broken down to posts_to_matrix
# matrix_to_lda
# lda_extract_topics
def posts_to_topic(posts, topic_num=5, top_word=30):

    if topic_num < 0:
        raise ValueError("topic_num must be non-negative integer")

    if top_word < 0:
        raise ValueError("top_word must be non-negative integer")

    print('Working on word separation....')
    # catch error here
    try:
        ws = WS("./data")
    except FileNotFoundError:
        print("Can't find model. Please download Ckip model")
    posts = ws(posts)

    print('Working on Count Vectorization....')
    cv = CountVectorizer(max_df=0.7, min_df=0.05)
    posts = [' '.join(post) for post in posts]
    matrix = cv.fit_transform(posts)

    print('Creating LDA....')
    LDA = LatentDirichletAllocation(n_components=topic_num)
    LDA.fit(matrix)
    result = {'topics': {}}

    for index, topic in enumerate(LDA.components_):
        result['topics'][f'topic_{index+1}'] = [
            cv.get_feature_names_out()[i] for i in topic.argsort()[-top_word:]]
    result['create_time'] = str(datetime.now())
    return result
