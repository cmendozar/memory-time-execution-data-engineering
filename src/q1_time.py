import pandas as pd
import json

from typing import List, Tuple
from datetime import datetime
from collections import defaultdict

from utils import timer

import json_stream

# +Function 'json_to_df' executed in 2.026740 seconds
# Function 'format_date' executed in 0.251882 seconds
# Function 'get_top_10_dates' executed in 0.009095 seconds
# Function 'get_tweeter_user_per_day' executed in 0.012737 seconds
# Function 'get_tweeter_user_per_day' executed in 0.007754 seconds
# Function 'get_tweeter_user_per_day' executed in 0.007847 seconds
# Function 'get_tweeter_user_per_day' executed in 0.007590 seconds
# Function 'get_tweeter_user_per_day' executed in 0.007342 seconds
# Function 'get_tweeter_user_per_day' executed in 0.007265 seconds
# Function 'get_tweeter_user_per_day' executed in 0.006811 seconds
# Function 'get_tweeter_user_per_day' executed in 0.006890 seconds
# Function 'get_tweeter_user_per_day' executed in 0.006715 seconds
# Function 'get_tweeter_user_per_day' executed in 0.006573 seconds
# Function 'q1_time' executed in 2.368550 seconds

# 1) 2.368550 memory
# 2)


@timer
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
    return df


@timer
def get_top_10_dates(dates: pd.DataFrame) -> list:
    """
    Input: Dataframe with date columns from json file, this df
    need to be with whole register.
    Return: List of top 10 order by more tweets counts desc.
    """
    top_10 = dates.value_counts().index[:10]
    return list(top_10)


@timer
def format_date(data: pd.DataFrame) -> list:
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].dt.strftime("%Y-%m-%d")
    return data


@timer
def get_tweeter_user_per_day(date: str, data: pd.DataFrame) -> str:
    date_rows = data[data['date'] == date]
    grouped_df = date_rows.groupby('user_name').count()
    user = grouped_df.sort_values('date', ascending=False).head(1).index[0]
    return user


@timer
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    result = list()
    df = json_to_df(file_path)
    formatted_df = format_date(df)
    top_10_dates = get_top_10_dates(formatted_df['date'])
    for date in top_10_dates:
        user = get_tweeter_user_per_day(date, formatted_df)
        result.append((datetime.strptime(date, "%Y-%m-%d").date(), user))
    return result


if __name__ == "__main__":
    file_path = "data/farmers-protest-tweets-2021-2-4.json"
    result = q1_time(file_path)
    print(result)
