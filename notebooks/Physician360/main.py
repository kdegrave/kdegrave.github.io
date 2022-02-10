from helper_functions import load_sentiment_classifier, load_sentiment_thresholds
from helper_functions import load_topic_classifier, load_topic_thresholds
from helper_functions import reshape_and_save_data, convert_sentiment_output
from helper_functions import convert_topic_output, ItemSelector, process_text
from model_settings import sentiment_classifier_path, topic_classifier_path
from model_settings import out_file_path, log_file_path
from import_data import import_comment_data
import pandas as pd
import numpy as np
import logging
import time


from helper_functions import save_most_recent_timestamp
from helper_functions import get_most_recent_timestamp

logging.basicConfig(filename=log_file_path + 'logfile.log', filemode='a',
                    level=logging.INFO, format='%(asctime)s %(levelname)-4s %(name)-4s %(message)s')

logger = logging.getLogger(__name__)


def main():
    # Load classification models and thresholds
    topic_classifier = load_topic_classifier(topic_classifier_path)
    topic_themes, topic_thresholds = load_topic_thresholds(topic_classifier_path)

    sentiment_thresholds = load_sentiment_thresholds(sentiment_classifier_path)
    sentiment_classifier = load_sentiment_classifier(sentiment_classifier_path, topic_themes)

    # Get timestamp of last comment inserted
    most_recent_timestamp = get_most_recent_timestamp(log_file_path + 'timestamp.log')

    # Load in new comment data
    df = import_comment_data(most_recent_timestamp)

    # Process the data
    df['CleanText'] = df['commenttext'].apply(process_text)
    df['CleanText'] = df['CleanText'].replace(np.nan, '')

    df['RecommendStar_bin'] = np.nan
    df.loc[df['RecommendStar'] >= 4, 'RecommendStar_bin'] = 0
    df.loc[df['RecommendStar'] <= 3, 'RecommendStar_bin'] = 1
    df = df.fillna(-1).reset_index(drop=True)

    # Apply topic model
    predict_topic = topic_classifier.predict_proba(df['CleanText'])
    predict_topic = convert_topic_output(predict_topic, topic_thresholds)

    # Apply sentiment model
    predict_sentiment = [sentiment_classifier[i].predict_proba(df)[:, 1] for i in sentiment_classifier]
    predict_sentiment = convert_sentiment_output(predict_sentiment, sentiment_thresholds)

    # Combine original data with predictions
    dp = pd.DataFrame(predict_topic * predict_sentiment, columns=topic_themes)
    df = pd.concat([df, dp], axis=1).replace({0: np.nan}).drop('CleanText', axis=1)

    # Reshape and save data
    reshape_and_save_data(df, topic_themes, out_file_path)

    # Save last timestamp
    save_most_recent_timestamp(log_file_path + 'timestamp.log', df)


if __name__ == "__main__":
    try:
        logger.info('Starting main function')

        start_time = time.time()
        main()
        end_time = time.time()
        logger.info('Total runtime: {} seconds'.format(np.round(end_time - start_time)))
        logger.info('Exited without errors\n')
    except:
        logger.exception('Exited with errors\n')
