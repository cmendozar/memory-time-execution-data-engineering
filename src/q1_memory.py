import json
from collections import Counter, defaultdict
from typing import List, Tuple
from datetime import datetime

from memory_profiler import profile
from utils import timer


def count_dates(file_path: str) -> dict:
    date_user_counters = defaultdict(Counter)
    with open(file_path, "r") as file:
        for line in file:
            try:
                tweet = json.loads(line)
                date = datetime.fromisoformat(tweet['date']).date()
                user_name = tweet.get("user", {}).get("username", "unknown")
                date_user_counters[date][user_name] += 1
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
            except KeyError as e:
                print(f"Missing 'date' key in JSON: {line}. Error: {e}")
    return date_user_counters


def get_top_10_dates(date_user_counters: dict) -> List[Tuple[datetime.date, int]]:
    all_dates = [(date, sum(user_counter.values())) for date, user_counter in date_user_counters.items()]
    all_dates.sort(key=lambda x: x[1], reverse=True)
    return all_dates[:10]


def get_top_users_per_date(
        date_user_counters: dict) -> List[Tuple[datetime.date, str]]:
    result = []
    top_10_dates = get_top_10_dates(date_user_counters)
    for date, count in top_10_dates:
        user_counter = date_user_counters[date]
        top_user = user_counter.most_common(1)[0][0]\
            if user_counter else "unknown"
        result.append((date, top_user))
    return result


@timer
@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    dates_data = count_dates(file_path)
    result = get_top_users_per_date(dates_data)
    return result


if __name__ == "__main__":
    file_path = "data/farmers-protest-tweets-2021-2-4.json"
    result = q1_memory(file_path)
    print(result)
