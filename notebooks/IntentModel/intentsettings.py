# Directory where the report excel file is stored
file_def = 'metricReporting/reportgen/MetricDefinitions.xlsx'
file_out = 'metricReporting/reportgen/IntentModelReport.xlsx'

# Sheet names
sheet_1 = "Metric Definitions"
sheet_2 = "Website Metrics"

# Header start cells for path and metrics (row, col)
start_p = (1, 2)
start_m = (27, 2)

tree_p = {'main': ['PathDirection'],
          'elems': ['In', 'Out'],
          'values': ['SourceName', 'MetricValue', 'PercentTotalNode', 'PercentTotal', 'PercentChangePrior'],
          'header1': ['Path'],
          'header2': ['In', 'Out'],
          'header3': ['Source', 'Volume', '% Node', '% Total', '% Change']}

# The "elems" list must follow the same order as header2
tree_m = {'main': ['IntentModelMetricType'],
          'elems': ['K', 'R', 'E', 'D'],
          'values': ['MetricName', 'MetricValue', 'PercentChangePrior'],
          'header1': ['Metrics'],
          'header2': ['Key Performance Indicator', 'Revenue', 'Engagement', 'Descriptive'],
          'header3': ['Source', 'Value', '% Change']}

# Specify which columns will be percentages
percent_p = ['PercentTotal', 'PercentTotalNode', 'PercentChangePrior']
percent_m = ['PercentChangePrior']
