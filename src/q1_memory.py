import pandas as pd
import json

from typing import List, Tuple
from datetime import datetime

from memory_profiler import profile, memory_usage


def json_to_df(file_path: str) -> pd.DataFrame:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            tweet_dict = {}
            try:
                tweet = json.loads(line)
                tweet_dict['date'] = tweet['date']
                tweet_dict['user_name'] = tweet.get(
                    'user', 'unknown'
                ).get('username', 'unknown')
                data.append(tweet_dict)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in line: {line}")
    df = pd.DataFrame(data)
    return df

@profile
def get_top_10_dates(dates: pd.DataFrame) -> list:
    """
    Input: Dataframe with date columns from json file, this df
    need to be with whole register.
    Return: List of top 10 order by more tweets counts desc.
    """
    top_10 = dates.value_counts().index[:11]
    return list(top_10)

@profile
def format_date(data: pd.DataFrame) -> list:
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].dt.strftime("%Y-%m-%d")
    return data

@profile
def get_tweeter_user_per_day(date: str, data: pd.DataFrame) -> str:
    date_rows = data[data['date'] == date]
    grouped_df = date_rows.groupby('user_name').count()
    user = grouped_df.sort_values('date', ascending=False).head(1).index[0]
    return user

@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    result = list()
    df = json_to_df(file_path)
    formatted_df = format_date(df)
    top_10_dates = get_top_10_dates(formatted_df['date'])
    for date in top_10_dates:
        user = get_tweeter_user_per_day(date, formatted_df)
        result.append((datetime.strptime(date, "%Y-%m-%d").date(), user))
    return result


if __name__ == '__main__':
    result = q1_memory('data/farmers-protest-tweets-2021-2-4.json')
    print(result)
