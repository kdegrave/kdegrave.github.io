import pandas as pd
import logging
import pyodbc

logger = logging.getLogger(__name__)


def import_comment_data(last_timestamp):
    logger.info('import_comment_data started')

    conn = pyodbc.connect()

    sql = """
            SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
            SELECT sp.NPI, sp.ProviderCode, usc.CommentID, usc.InsertedOn,
            usc.commenttext, usc.UserSurveyID, us.RecommendStar
            FROM pes.inv.usersurvey us
            JOIN pes.inv.usersurveycomment usc on us.usersurveyid = usc.usersurveyid
            JOIN ods1.show.solrprovider sp on us.providercode = sp.providercode
            AND sp.DisplayStatusCode = 'A' and sp.SubStatusCode not in ('L','B','L5')
            WHERE usc.InsertedOn >= ?
            AND us.suppressionreasoncode is null
            AND usc.commentstatusid in (3,5)
            AND us.isconfirmed = 1
            AND us.ispublished = 1
          """

    df = pd.read_csv('Physician360/reviews.csv')

    df = df[~df['commenttext'].isnull()].reset_index(drop=True)
    
    df.rename(columns={'survey_starscore': 'RecommendStar'}, inplace=True)

    logger.info('import_comment_data finished')
    return df
