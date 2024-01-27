import pytest # noqa
import ptt_topic_modeling.ptt_lda as ptt_lda
from datetime import datetime


@pytest.mark.xfail  # missing model file in repo
class TestPostsToTopic(object):
    def test_check_topic_n_word_num_n_time(self):
        data = ['是因為政府做得好 還是貧富差距沒有想像中大呢',
                '你敢衝上去壓制嗎 還是在旁邊喊不要動就好']
        result = ptt_lda.posts_to_topic(data, 2, 5)
        assert len(result['topics']) == 2, \
            f"expecting 5 topics, instead got {len(result['topics'])}"

        assert len(result['topics']['topic_1']) == 5, \
            "expecting top 30 words per topic" + \
            f", instead got {len(result['topics']['topic_1'])}"
        date = datetime.strptime(result['create_time'].split(' ')[0],
                                 "%Y-%m-%d")
        assert isinstance(date, datetime)
