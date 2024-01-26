import sys
import ptt_topic_modeling.ptt_lda as ptt_lda
import warnings


def main():
    # Ckiptagger will produce tensorflow deprication warning
    warnings.filterwarnings("ignore", category=UserWarning)

    output_path = './result.json'

    posts = ptt_lda.board_to_post(sys.argv[1], int(sys.argv[2]))
    topics = ptt_lda.posts_to_topic(posts)
    ptt_lda.to_json(topics, output_path)
    print(f'file saved to {output_path}')

    for i in range(1, 6):
        print(f'TOPIC #{i} 前30名詞彙')
        print(topics[f'topic_{i}'])
        print('\n')


if __name__ == "__main__":
    main()
