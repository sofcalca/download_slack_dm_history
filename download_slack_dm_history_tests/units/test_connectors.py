# coding=utf-8

import unittest
from unittest.mock import MagicMock, patch, call

from download_slack_dm_history.connectors import ChannelNotFound, retrieve_all_slack_messages, InvalidToken, \
    UnknownConnectorError


class RetrieveAllSlackMessagesTest(unittest.TestCase):

    @patch("download_slack_dm_history.connectors.requests")
    def test_should_raise_channel_not_found_when_given_wrong_channel_id(self, mocked_requests):
        # Given
        response = MagicMock()
        response.status_code = 200
        response.json = MagicMock(return_value={'ok': False, 'error': 'channel_not_found'})
        mocked_requests.get = MagicMock(return_value=response)
        channel_id = "abc"
        token = "zxc123"

        # When
        with self.assertRaises(ChannelNotFound):
            messages = retrieve_all_slack_messages(channel_id, token)
            # Then
            self.assertIsNone(messages)

    @patch("download_slack_dm_history.connectors.requests")
    def test_should_raise_invalid_token_when_given_wrong_token(self, mocked_requests):
        # Given
        response = MagicMock()
        response.status_code = 200
        response.json = MagicMock(return_value={'ok': False, 'error': 'invalid_auth'})
        mocked_requests.get = MagicMock(return_value=response)
        channel_id = "abc"
        token = "zxc123"

        # When
        with self.assertRaises(InvalidToken):
            messages = retrieve_all_slack_messages(channel_id, token)
            # Then
            self.assertIsNone(messages)

    @patch("download_slack_dm_history.connectors.requests")
    def test_should_raise_unknown_connector_error_when_return_value_is_not_ok_and_other_error(self, mocked_requests):
        # Given
        response = MagicMock()
        response.status_code = 200
        response.json = MagicMock(return_value={'ok': False, 'error': 'unknown_error'})
        mocked_requests.get = MagicMock(return_value=response)
        channel_id = "abc"
        token = "zxc123"

        # When
        with self.assertRaises(UnknownConnectorError):
            messages = retrieve_all_slack_messages(channel_id, token)
            # Then
            self.assertIsNone(messages)

    @patch("download_slack_dm_history.connectors.requests")
    def test_should_call_slack_api_once_if_no_more_messages(self, mocked_requests):
        # Given
        response = MagicMock()
        response.status_code = 200
        slack_messages = [
            {
                'client_msg_id': 'abc-1def-2gh3',
                'type': 'message',
                'text': 'hello',
                'user': 'ABC1DEF',
                'ts': '1579718270.000600',
                'team': 'ZXC1BU',
                'blocks': [
                    {
                        'type': 'rich_text',
                        'block_id': 'a1',
                        'elements': [
                            {
                                'type': 'rich_text_section',
                                'elements': [
                                    {
                                        'type': 'text',
                                        'text': 'hello'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        response.json = MagicMock(return_value={
            'ok': True,
            'messages': slack_messages,
            'has_more': False,
            'pin_count': 0,
            'channel_actions_ts': None,
            'channel_actions_count': 0
        }
)
        mocked_requests.get = MagicMock(return_value=response)
        channel_id = "abc"
        token = "zxc123"
        expected_url_called = 'https://slack.com/api/conversations.history?token=zxc123&channel=abc'

        # When
        retrieved_messages = retrieve_all_slack_messages(channel_id, token)

        # Then
        mocked_requests.get.assert_called_once_with(expected_url_called)
        self.assertEquals(slack_messages, retrieved_messages)

    @patch("download_slack_dm_history.connectors.requests")
    def test_should_call_slack_api_again_if_has_more_messages(self, mocked_requests):
        # Given
        response = MagicMock()
        response.status_code = 200
        slack_messages_from_first_call = [
            {
                'client_msg_id': 'abc-1def-2gh3',
                'type': 'message',
                'text': 'hello',
                'user': 'ABC1DEF',
                'ts': '1579718270.000600',
                'team': 'ZXC1BU',
                'blocks': [
                    {
                        'type': 'rich_text',
                        'block_id': 'a1',
                        'elements': [
                            {
                                'type': 'rich_text_section',
                                'elements': [
                                    {
                                        'type': 'text',
                                        'text': 'hello'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        slack_messages_from_second_call = [
            {
                'client_msg_id': 'abc-1def-2gh3',
                'type': 'message',
                'text': "it's me",
                'user': 'ABC1DEF',
                'ts': '1579718270.000600',
                'team': 'ZXC1BU',
                'blocks': [
                    {
                        'type': 'rich_text',
                        'block_id': 'a1',
                        'elements': [
                            {
                                'type': 'rich_text_section',
                                'elements': [
                                    {
                                        'type': 'text',
                                        'text': "it's me"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        response.json = MagicMock(side_effect=[
            {
                'ok': True,
                'messages': slack_messages_from_first_call,
                'has_more': True,
                'pin_count': 0,
                'channel_actions_ts': None,
                'channel_actions_count': 0,
                'response_metadata': {'next_cursor': 'a1b2c3'}
            },
            {
                'ok': True,
                'messages': slack_messages_from_second_call,
                'has_more': False,
                'pin_count': 0,
                'channel_actions_ts': None,
                'channel_actions_count': 0
            }
        ]
)
        mocked_requests.get = MagicMock(return_value=response)
        channel_id = "abc"
        token = "zxc123"
        expected_calls = [
            call('https://slack.com/api/conversations.history?token=zxc123&channel=abc'),
            call('https://slack.com/api/conversations.history?token=zxc123&channel=abc&cursor=a1b2c3')
        ]

        # When
        retrieved_messages = retrieve_all_slack_messages(channel_id, token)

        # Then
        mocked_requests.get.assert_has_calls(expected_calls)
        self.assertEquals(slack_messages_from_first_call + slack_messages_from_second_call, retrieved_messages)
