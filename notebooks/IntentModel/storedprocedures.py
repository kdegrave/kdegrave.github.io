from intentsettings import *
import pandas as pd
import pyodbc


def stored_procedures():

    conn = pyodbc.connect()

    # Run stored procedures to get data. Variable "inNumberOfWeeeks" is hardcoded as 4.
    sql_path = "EXEC ReportingMetric.im.ProcGetIntentReportSection \
                @inNodeName = 'All', \
                @inSectionName = 'Path', \
                @inNumberOfWeeks = 4"

    sql_metric = "EXEC ReportingMetric.im.ProcGetIntentReportSection \
                    @inNodeName = 'All', \
                    @inSectionName = 'Metric', \
                    @inNumberOfWeeks = 4"

    df_p = pd.read_sql(sql_path, conn)
    df_m = pd.read_sql(sql_metric, conn)

    df_p = df_p[['NodeName', 'MetricType'] + tree_p['main'] + tree_p['values']]
    df_m = df_m[['NodeName', 'MetricType'] + tree_m['main'] + tree_m['values']]
    return df_p, df_m
