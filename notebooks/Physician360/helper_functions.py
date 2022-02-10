from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator
from datetime import datetime
from joblib import load
import sys, re, os
import numpy as np
import logging


logger = logging.getLogger(__name__)


class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


def process_text(text):
    text = text.lower().strip()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = re.sub(r'\\+', ' ', text)
    text = re.sub(r'\.+', ' ', text)
    text = re.sub(r'\!+', ' ', text)
    text = re.sub(r'\?+', ' ', text)
    text = re.sub(r'\-+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r' +', ' ', text).strip()
    return text


def load_topic_thresholds(path):
    logger.info('load_topic_thresholds started')

    topic_thresholds = load(path + 'topic_thresholds.joblib')

    topic_themes = list(topic_thresholds.keys())
    topic_thresholds = list(topic_thresholds.values())
    logger.info('load_topic_thresholds finished')
    return topic_themes, topic_thresholds


def load_topic_classifier(path):
    logger.info('load_topic_classifier started')

    topic_classifier = load(path + 'topic_classifier.joblib')
    logger.info('load_topic_classifier finished')
    return topic_classifier


def load_sentiment_thresholds(path):
    logger.info('load_sentiment_thresholds started')

    sentiment_thresholds = load(path + 'sentiment_thresholds.joblib')
    logger.info('load_sentiment_thresholds finished')
    return sentiment_thresholds


def load_sentiment_classifier(path, topic_themes):
    logger.info('load_sentiment_classifier started')

    sentiment_classifier = {}

    for i in topic_themes:
        sentiment_classifier[i] = load(path + i + '_sentiment_classifier.joblib')
    logger.info('load_sentiment_classifier finished')
    return sentiment_classifier


def convert_topic_output(predict_topic, topic_thresholds):
    logger.info('convert_topic_output started')

    predict_topic = np.column_stack([(predict_topic[:, i] >=
                                      topic_thresholds[i]).astype(int) for i in range(len(topic_thresholds))])
    logger.info('convert_topic_output finished')
    return predict_topic


def convert_sentiment_output(predict_sentiment, sentiment_thresholds):
    logger.info('convert_sentiment_output started')

    predict_sentiment = np.column_stack([(predict_sentiment[i] >=
                                         sentiment_thresholds[j]).astype(int) for i, j in
                                         enumerate(sentiment_thresholds)])

    # Map predictions from 0, 1 to 1, -1
    predict_sentiment[predict_sentiment == 1] = -1
    predict_sentiment[predict_sentiment == 0] = 1
    logger.info('convert_sentiment_output finished')
    return predict_sentiment


def reshape_and_save_data(df, topic_themes, out_file_path):
    logger.info('reshape_and_save_data started')

    time_now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    # Comment out if we don't want to melt dataframe
    # df = df.melt(id_vars=df.drop(topic_themes, axis=1).columns, var_name="Theme",
    #        value_name="Sentiment").sort_values('CommentID').dropna(subset=['Sentiment']).reset_index(drop=True)

    df['ScoreDate'] = time_now

    # Drop comment text before saving
    df.drop(['commenttext', 'RecommendStar', 'RecommendStar_bin'],
                    axis=1).to_csv(out_file_path + 'output' + '_' + time_now + '.csv', index=False)
    logger.info('reshape_and_save_data finished')


def get_most_recent_timestamp(filename):
    logger.info('get_most_recent_timestamp started')

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'rb') as f:
            last_line = f.readlines()[-1].decode().strip()
        logger.info('get_most_recent_timestamp finished')
        return last_line
    else:
        logger.info('Creating timestamp file & scoring all reviews')
        return sys.argv[1]


def save_most_recent_timestamp(filename, df):
    logger.info('save_most_recent_timestamp started')

    if os.path.exists(filename):
        file = open(filename, 'a')
    else:
        file = open(filename, 'w')

    #file.write(df['InsertedOn'].max().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    #file.close()
    logger.info('save_most_recent_timestamp finished')
