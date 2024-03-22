import json
import re

from typing import List, Tuple
from utils import timer
from memory_profiler import profile

from collections import Counter

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

@timer
@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    pattern = EMOJI_PATTERN
    emoji_counts = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                text = tweet.get('renderedContent', '').replace('\n', '')
                emoji_counts.update(re.findall(pattern, text))
                tweet_content = tweet.get('quotedTweet', False)
                if tweet_content:
                    emoji_counts.update(
                        re.findall(
                            pattern,
                            tweet_content.get('renderedContent', '')
                        )
                    )
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
    return emoji_counts.most_common(10)


if __name__ == '__main__':
    file_path = 'data/farmers-protest-tweets-2021-2-4.json'
    result = q2_memory(file_path)
    print(result)
