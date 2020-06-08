from typing import List

import requests


def build_request(channel_id: str, next_cursor: str, token: str) -> str:
    request = f"https://slack.com/api/conversations.history?token={token}&channel={channel_id}"
    if next_cursor:
        request += f'&cursor={next_cursor}'
    return request


def retrieve_all_slack_messages(channel_id: str, token:str) -> List[dict]:
    has_more = True
    messages = []
    next_cursor = ''
    while has_more:
        request = build_request(channel_id, next_cursor, token)
        response = requests.get(request)
        response_json = response.json()
        has_more = response_json["has_more"]
        if has_more:
            next_cursor = response_json['response_metadata']['next_cursor']
        messages = messages + response_json["messages"]
    return messages