import pytest # noqa
import ptt_topic_modeling.crawler as crawler


class TestLinksToPosts(object):
    def test_array_length_n_type(self):
        links = {
            'link1': 'https://www.ptt.cc/bbs/Gossiping/M.1706344390.A.929.html', # noqa
            'link2': 'https://www.ptt.cc/bbs/Gossiping/M.1706344471.A.4C2.html'} # noqa
        result = crawler.links_to_posts(links)
        assert len(result) == len(links), \
            f'expecting 20 posts, got {len(result)} posts'

        assert isinstance(result[0], str), \
            f'expecting string, got {type(result[0])}'

        assert isinstance(result[-1], str), \
            f'expecting string, got {type(result[-1])}'


class TestCrawlLink(object):
    def test_correct_length(self):
        result = crawler.crawl_links('Gossiping', 20)
        assert len(result) == 20, \
            f'expecting 20 links, got {len(result)} links'

    def test_bad_length(self):
        with pytest.raises(ValueError) as excinfo:
            crawler.crawl_links('Gossiping', -10)
        assert str(excinfo.value) == "target_num must be non-negative integer"

    def test_wrong_board_name(self):
        with pytest.raises(ConnectionError) as excinfo:
            crawler.crawl_links('Gossip')
        assert str(excinfo.value) == 'webpage not available'


class TestCrawlPage(object):

    def test_output_type(self):
        link = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        next, links = crawler.crawl_page(link)
        assert isinstance(next, str), \
            f'expecting string, got {type(next)}'

        assert isinstance(links, dict), \
            f'expecting string, got {type(links)}'

    def test_no_next_page(self):
        link = 'https://www.ptt.cc/man/Gossiping/D42E/D454/' + \
            'M.1675168627.A.117.html'
        with pytest.raises(TypeError) as excinfo:
            crawler.crawl_page(link)
        assert str(excinfo.value) == "Can't find next page."
    pass


class TestCrawlPost(object):
    def test_check_combined_instance(self):
        link = 'https://www.ptt.cc/man/Gossiping/D42E/D454/' + \
            'M.1675168627.A.117.html'
        result = crawler.crawl_post(link)

        assert len(result) == 1, \
            f'expecting two items in list, got {len(result)}'

        assert isinstance(result[0], str)

    def test_check_split_instance(self):
        link = 'https://www.ptt.cc/man/Gossiping/D42E/D454/' + \
            'M.1675168627.A.117.html'
        result = crawler.crawl_post(link, combine_text=False)

        assert isinstance(result, list), \
            f'expecting list, got {type(result)}'

        assert len(result) == 2, \
            f'expecting two items in list, got {len(result)}'

        assert isinstance(result[0], str), \
            f'expecting string, got {type(result[0])}'

        assert isinstance(result[1], list), \
            f'expecting list, got {type(result[1])}'


class TestSendRequest(object):

    def test_successful(self):
        link = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        resp = crawler.send_request(link)
        assert resp.status_code == 200

    def test_failed_link(self):
        link = 'not_a_link'
        with pytest.raises(ValueError) as excinfo:
            crawler.send_request(link)
        assert str(excinfo.value) == f'{link} does not belong to PTT'

    def test_link_to_elsewhere(self):
        link = 'https://www.google.com'
        with pytest.raises(ValueError) as excinfo:
            crawler.send_request(link)
        assert str(excinfo.value) == f'{link} does not belong to PTT'

    def test_bad_ptt_link(self):
        link = 'https://www.ptt.cc/bbs/asdkc/index.html'
        with pytest.raises(ConnectionError) as excinfo:
            crawler.send_request(link)
        assert str(excinfo.value) == 'webpage not available', \
            f'expecting "webpage not available", got {str(excinfo.value)}'


'''
def test_(self):
    actual = func()
    expected =
    message = f" INPUT \
        return {actual} instead of {expected}"
    assert actual == expected, message
'''
