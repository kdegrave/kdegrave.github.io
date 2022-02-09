from storedprocedures import stored_procedures
from populateworkbook import create_workbook
from populateworkbook import setup_p_data
from populateworkbook import setup_m_data
from formatworkbook import format_workbook
from sendemail import send_email
from intentsettings import *
from emailsettings import *

def main():
	# Get path and metrics data from stored procedures
	df_p, df_m = stored_procedures()

	# Format data percentages
	df_p.loc[df_p['MetricType'] == 'percent', 'MetricValue'] = \
		df_p.loc[df_p['MetricType'] == 'percent', 'MetricValue'].astype(str) + '%%'

	df_m.loc[df_m['MetricType'] == 'percent', 'MetricValue'] = \
		df_m.loc[df_m['MetricType'] == 'percent', 'MetricValue'].astype(str) + '%%'

	df_p[percent_p] = df_p[percent_p].astype(str) + '%%'
	df_m[percent_m] = df_m[percent_m].astype(str) + '%%'

	df_p.drop('MetricType', axis=1, inplace=True)
	df_m.drop('MetricType', axis=1, inplace=True)

	data_p, depth_p = setup_p_data(df_p)
	data_m, depth_m = setup_m_data(df_m)

	wb = create_workbook(data_p, data_m)

	format_workbook(wb, start_p, start_m, tree_p, tree_m, depth_p, depth_m)

	send_email(send_from, send_to, subject, message, files=[file_out],
			  			server=server, port=port, username=username,
			  			password=password, use_tls=True)

if __name__ == "__main__":
	main()