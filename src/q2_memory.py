import json
import re

from typing import List, Tuple
from utils import timer
from memory_profiler import profile

from collections import Counter


@timer
@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counts = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                text = tweet.get('renderedContent', '').replace('\n', '')
                emoji_counts.update(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]+', text))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
    return emoji_counts.most_common(10)


if __name__ == '__main__':
    file_path = 'data/farmers-protest-tweets-2021-2-4.json'
    result = q2_memory(file_path)
    print(result)