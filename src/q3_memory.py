import json
import re
from typing import List, Tuple
from utils import timer
from memory_profiler import profile
from collections import Counter


@timer
@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    user_counts = Counter()
    pattern = r'\B@([a-zA-Z0-9_]+)\b'
    with open(file_path, 'r') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                users = re.findall(pattern, tweet.get('renderedContent', ''))
                user_counts.update(users)
                quoted_tweet = tweet.get('quotedTweet')
                if quoted_tweet:
                    quoted_users = re.findall(pattern, quoted_tweet.get('renderedContent', ''))
                    user_counts.update(quoted_users)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
    return user_counts.most_common(10)


if __name__ == '__main__':
    file_path = 'data/farmers-protest-tweets-2021-2-4.json'
    result = q2_memory(file_path)
    print(result)
