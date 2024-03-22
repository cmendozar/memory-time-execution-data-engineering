
import json
import re

from typing import List, Tuple
from utils import timer
from memory_profiler import profile

EMOJI_PATTERN = re.compile(
    # Got it from: https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1
    "(["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "])"
)


def count_emojis(text: str) -> List[Tuple[str, int]]:
    emoticons = re.finditer(EMOJI_PATTERN, text)
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
                tweet_content = tweet.get('quotedTweet', False)
                if tweet_content:
                    data.append(tweet_content.get('renderedContent', ''))
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