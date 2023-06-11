import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
import tensorflow as tf
import random
from sklearn.preprocessing import LabelEncoder, StandardScaler

from src.db.connection import DB_URL
from src.ml.query import *

ML_MODEL = tf.keras.models.load_model('src/assets/model.h5')

def get_ml_data() -> pd.DataFrame:
    connection = create_engine(DB_URL).connect()
    query = text(ml_model_data_query())
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return df

def get_ml_recommendation_data(username: str) -> pd.DataFrame:
    connection = create_engine(DB_URL).connect()
    query = text(ml_recommendation_data_query(username=username))
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return df

def get_ml_recommended_data(user_ids: str) -> pd.DataFrame:
    connection = create_engine(DB_URL).connect()
    query = text(get_list_of_recommendations(user_ids=user_ids))
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return df

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    raw_data = data.copy()

    label_encoder_user = LabelEncoder()
    label_encoder_field = LabelEncoder()
    label_encoder_city = LabelEncoder()
    raw_data['User ID'] = label_encoder_user.fit_transform(raw_data['User ID'])
    raw_data['Field'] = label_encoder_field.fit_transform(raw_data['Field'])
    raw_data['City'] = label_encoder_city.fit_transform(raw_data['City'])

    # Initialize the Scaler
    scaler = StandardScaler()

    # Fit the scaler to the followers count features and transform them
    raw_data['num_followers_instagram'] = scaler.fit_transform(raw_data[['num_followers_instagram']])
    raw_data['num_followers_twitter'] = scaler.fit_transform(raw_data[['num_followers_twitter']])
    raw_data['num_followers_tiktok'] = scaler.fit_transform(raw_data[['num_followers_tiktok']])

    return raw_data

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

def model_predict(user_ids: list):
    data = preprocess(data=get_ml_data())

    fields, cities, \
    instagram, twitter, tiktok, \
    num_followers_tiktok, num_followers_instagram, \
    num_followers_twitter = filter_data(user_ids, data)

    predictions = ML_MODEL.predict([
        np.array(user_ids), fields, cities, instagram, twitter, tiktok,
        num_followers_tiktok, num_followers_instagram,
        num_followers_twitter
    ])

    return np.argmax(predictions, axis=1).tolist()

def list_to_tuple_string(recommended_list: list) -> str:
    STR = '('

    for num in recommended_list:
        STR += f'{num}, '
    STR = STR[:-2] + ')'
    
    return STR

def ml_recommendation(username: str):
    connection = create_engine(DB_URL).connect()
    query = text(check_user_has_liked(username=username))
    check_username = connection.execute(query)
    connection.close()
    if check_username.fetchone()[0] != 0:
        data = preprocess(data=get_ml_recommendation_data(username=username))
        user_ids_liked = data['User ID'].values
    else:
        data = preprocess(data=get_ml_data())
        user_ids_liked = [random.randint(1, 100) for _ in range(5)]

    fields, cities, \
    instagram, twitter, tiktok, \
    num_followers_tiktok, num_followers_instagram, \
    num_followers_twitter = filter_data(user_ids_liked, data)

    predictions = ML_MODEL.predict([
        np.array(user_ids_liked), fields, cities, instagram, twitter, tiktok,
        num_followers_tiktok, num_followers_instagram,
        num_followers_twitter
    ])

    df_recommended = get_ml_recommended_data(list_to_tuple_string(np.argmax(predictions, axis=1).tolist()))
    return df_recommended.to_dict(orient='records')
