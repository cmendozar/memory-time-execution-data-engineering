import pandas as pd
import json

from typing import List, Tuple
from datetime import datetime

from memory_profiler import profile
from utils import timer


def json_to_df(file_path: str) -> pd.DataFrame:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            tweet_dict = {}
            try:
                tweet = json.loads(line)
                tweet_dict['date'] = tweet['date']
                tweet_dict['user_name'] = tweet.get(
                    'user', {}
                ).get('username', 'unknown')
                data.append(tweet_dict)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in line: {line}")
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df


def get_top_10_dates(dates: pd.DataFrame) -> list:
    """
    Input: Dataframe with date columns from json file, this df
    need to be with whole register.
    Return: List of top 10 order by more tweets counts desc.
    """
    top_10 = dates.value_counts().index[:10]
    return list(top_10)


def get_tweeter_user_per_day(date: str, data: pd.DataFrame) -> str:
    date_rows = data[data['date'] == date]
    grouped_df = date_rows.groupby('user_name').count()
    user = grouped_df.sort_values('date', ascending=False).head(1).index[0]
    return user


@timer
@profile
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    result = list()
    df = json_to_df(file_path)
    date_df = df['date']
    top_10_dates = get_top_10_dates(date_df)
    for date in top_10_dates:
        user = get_tweeter_user_per_day(date, df)
        result.append((date, user))
    return result


if __name__ == '__main__':
    file_path = 'data/farmers-protest-tweets-2021-2-4.json'
    result = q1_time(file_path)
    print(result)
