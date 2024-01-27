import pytest # noqa
import json
import os
import ptt_topic_modeling.utils as utils


class TestFullToHalf(object):

    def test_no_change(self):
        actual = utils.full_to_half('(test, this.)')
        expected = '(test, this.)'
        message = "full_to_half('(test, this.)'" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_exclam_and_ques(self):
        actual = utils.full_to_half('(test？ this！)')
        expected = '(test? this!)'
        message = "full_to_half('(test？ this！)'" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_brackets(self):
        actual = utils.full_to_half('（test, this.）')
        expected = '(test, this.)'
        message = "full_to_half('（test, this.）'" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message


class TestRemoveHtml(object):

    def test_no_change(self):
        actual = utils.remove_html('http is not a url.')
        expected = 'http is not a url.'
        message = "remove_html('http is not a url.'" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_http(self):
        actual = utils.remove_html('link: http://www.youtube.com')
        expected = 'link: '
        message = "remove_html('link: http://www.youtube.com')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_https(self):
        actual = utils.remove_html('link:https://www.youtube.com')
        expected = 'link:'
        message = "remove_html('link:https://www.youtube.com')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message


class TestStripMultiSpaces(object):

    def test_no_change(self):
        actual = utils.strip_multi_spaces('all single spaces.')
        expected = 'all single spaces.'
        message = "strip_multi_spaces('all single spaces.')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_middle_multi(self):
        actual = utils.strip_multi_spaces('all        spaces.')
        expected = 'all spaces.'
        message = "strip_multi_spaces('all        spaces.')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_preced_follow_spaces(self):
        actual = utils.strip_multi_spaces('    all   spaces.  ')
        expected = ' all spaces. '
        message = ".strip_multi_spaces('    all   spaces.  ')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message


class TestStripPunctuation(object):

    def test_no_change(self):
        actual = utils.strip_punctuation('no punc here')
        expected = 'no punc here'
        message = "strip_punctuation('no punc here'" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_accident_multi(self):
        actual = utils.strip_punctuation('(((test, this.)))')
        expected = ' test  this '
        message = "strip_punctuation('(((test, this.)))')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message

    def test_emoticon(self):
        actual = utils.strip_punctuation('@@ ^_^ :)')
        expected = '     '
        message = "strip_punctuation('@@ ^_^ :)')" + \
            f"return '{actual}' instead of '{expected}'"
        assert actual == expected, message


class TestToJson(object):
    def test_normal(self, tmpdir):
        data = {'a': 1, 'b': 2}
        file = tmpdir.join('output.json')
        utils.to_json(data, file)
        expected = {'a': 1, 'b': 2}
        assert os.path.exists(file), 'export file failed'

        with open(file) as f:
            loaded_data = json.load(f)
        assert loaded_data == expected, 'data read does not match data written'


'''
def test_(self):
    actual = func()
    expected =
    message = "INPUT" +\
        "return {actual} instead of {expected}"
    assert actual == expected, message
'''
