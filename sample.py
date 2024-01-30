import sys
import ptt_topic_modeling.utils as utils
import ptt_topic_modeling.ptt_lda as ptt_lda
import ptt_topic_modeling.crawler as crawler
import warnings


def main():
    # Ckiptagger will produce tensorflow deprication warning

    warnings.filterwarnings("ignore", category=UserWarning)

    output_path = './result.json'

    links = crawler.crawl_links(sys.argv[1], int(sys.argv[2]))
    posts = crawler.links_to_posts(links)
    topics = ptt_lda.posts_to_topic(posts)
    utils.to_json(topics, output_path)
    print(f'file saved to {output_path}')

    for i in range(1, 6):
        print(f'TOPIC #{i} 前30名詞彙')
        print(topics['topics'][f'topic_{i}'])
        print('\n')


if __name__ == "__main__":
    main()
