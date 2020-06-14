def build_request(channel_id: str, next_cursor: str, token: str) -> str:
    request = f"https://slack.com/api/conversations.history?token={token}&channel={channel_id}"
    if next_cursor:
        request += f'&cursor={next_cursor}'
    return request


