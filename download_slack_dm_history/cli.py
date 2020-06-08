#!/usr/bin/python
# coding=utf-8
import json

import click

from download_slack_dm_history.utils import retrieve_all_slack_messages


@click.group()
def cli():
    pass


@click.command('download_history')
@click.option('--output_file_path')
@click.option('--channel_id')
@click.option('--token')
def download_history(token: str, channel_id: str, output_file_path: str):
    messages = retrieve_all_slack_messages(channel_id, token)
    write_messages_to_file(messages, output_file_path)


def write_messages_to_file(messages, output_file_path):
    with open(output_file_path, "w+") as file:
        json.dump(messages, file)
    file_path = output_file_path
    print(f'Wrote conversation history in {file_path}')


cli.add_command(download_history)

if __name__ == '__main__':
    cli()
