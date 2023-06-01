import numpy as np
import pandas as pd

def get_data() -> pd.DataFrame:
    return "TODO"

def filter_data(user_ids: list, data: pd.DataFrame):
    fields = data.loc[data['User ID'].isin(user_ids), 'Field'].values
    cities = data.loc[data['User ID'].isin(user_ids), 'City'].values
    instagram = data.loc[data['User ID'].isin(user_ids), 'is_have_instagram'].values
    twitter = data.loc[data['User ID'].isin(user_ids), 'is_have_twitter'].values
    tiktok = data.loc[data['User ID'].isin(user_ids), 'is_have_tiktok'].values
    num_followers_tiktok = data.loc[data['User ID'].isin(user_ids), 'num_followers_tiktok'].values
    num_followers_instagram = data.loc[data['User ID'].isin(user_ids), 'num_followers_instagram'].values
    num_followers_twitter = data.loc[data['User ID'].isin(user_ids), 'num_followers_twitter'].values
    return fields, cities, instagram, twitter, tiktok, num_followers_tiktok, num_followers_instagram, num_followers_twitter

def model_inference(user_ids: list):
    data = get_data()
    fields, cities, \
    instagram, twitter, tiktok, \
    num_followers_tiktok, num_followers_instagram, \
    num_followers_twitter = filter_data(user_ids, data)