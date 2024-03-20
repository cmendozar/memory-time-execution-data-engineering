
import json
import re

from typing import List, Tuple
from utils import timer
from memory_profiler import profile


def count_emojis(text: str) -> List[Tuple[str, int]]:
    emoticons = re.finditer(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]+', text)
    emojis = [emoticon.group(0) for emoticon in emoticons]
    emoji_counts = {}
    for eji in emojis:
        if eji in emoji_counts:
            emoji_counts[eji] += 1
        else:
            emoji_counts[eji] = 1
    sorted_counts = sorted(
        emoji_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )
    return sorted_counts[:10]


def json_to_text(file_path: str) -> str:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                data.append(tweet.get('renderedContent', '').replace('\n', ''))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
    return ''.join(data)

@timer
@profile
def q2_time(file_path: str) -> List[Tuple[str, int]]:
    tweets_content = json_to_text(file_path)
    qty_emojis = count_emojis(tweets_content)
    return qty_emojis


if __name__ == '__main__':
    file_path = 'data/farmers-protest-tweets-2021-2-4.json'
    result = q2_time(file_path)
    print(result)