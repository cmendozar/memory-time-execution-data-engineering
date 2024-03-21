from typing import List, Tuple
import json
import re

from memory_profiler import profile
from utils import timer


def json_to_text(file_path: str) -> str:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                rendered_content = tweet.get('renderedContent', '')
                data.append(rendered_content)
                quoted_tweet = tweet.get('quotedTweet')
                if quoted_tweet:
                    data.append(quoted_tweet.get('renderedContent', ''))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
            except AttributeError as e:
                print(f"Error accessing attribute in line: {line}. Error: {e}")
    return ''.join(data)


def count_users(text: str) -> List[Tuple[str, int]]:
    pattern = r'\B@([a-zA-Z0-9_]+)\b'
    users = re.findall(pattern, text)
    users_counter = {}
    for user in users:
        if user in users_counter:
            users_counter[user] += 1
        else:
            users_counter[user] = 1
    sorted_counts = sorted(
        users_counter.items(),
        key=lambda item: item[1],
        reverse=True
    )
    return sorted_counts[:10]


@timer
@profile
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    tweets_content = json_to_text(file_path)
    users_qty = count_users(tweets_content)
    return users_qty


if __name__ == '__main__':
    file_path = 'data/farmers-protest-tweets-2021-2-4.json'
    result = q3_time(file_path)
    print(result)
