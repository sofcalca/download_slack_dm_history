from typing import List

import requests

from download_slack_dm_history.utils import build_request


def retrieve_all_slack_messages(channel_id: str, token: str) -> List[dict]:
    has_more = True
    messages = []
    next_cursor = ''
    while has_more:
        request = build_request(channel_id, next_cursor, token)
        response = requests.get(request)
        response_json = response.json()
        _check_errors(response_json)
        has_more = response_json["has_more"]
        if has_more:
            next_cursor = response_json['response_metadata']['next_cursor']
        messages = messages + response_json["messages"]
    return messages


def _check_errors(response_json):
    if response_json.get("ok") is False:
        if response_json.get("error") == 'channel_not_found':
            raise ChannelNotFound
        elif response_json.get("error") == 'invalid_auth':
            raise InvalidToken
        else:
            raise UnknownConnectorError


class ChannelNotFound(Exception):
    pass


class InvalidToken(Exception):
    pass


class UnknownConnectorError(Exception):
    pass