# coding=utf-8

import unittest

from download_slack_dm_history.utils import build_request


class BuildRequestTest(unittest.TestCase):
    def test_should_return_url_with_cursor_when_specified(self):
        # When
        request = build_request(channel_id='A1', next_cursor='abc1', token='xsoa65')
        
        # Then
        self.assertEqual('https://slack.com/api/conversations.history?token=xsoa65&channel=A1&cursor=abc1', request)
        pass

    def test_should_return_url_without_cursor_when_not_specified(self):
        # When
        request = build_request(channel_id='A1', next_cursor='', token='xsoa65')

        # Then
        self.assertEqual('https://slack.com/api/conversations.history?token=xsoa65&channel=A1', request)
