import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler

from src.db.connection import DB_URL
from src.ml.query import ml_model_data_query

ML_MODEL = tf.keras.models.load_model('src/assets/model.h5')

def get_ml_data() -> pd.DataFrame:
    connection = create_engine(DB_URL).connect()
    query = text(ml_model_data_query())
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