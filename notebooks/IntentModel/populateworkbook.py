from openpyxl import Workbook, load_workbook
from intentsettings import *
import pandas as pd
import numpy as np

def setup_p_data(df_p):
    main_p = tree_p['main'][0]
    elems_p = tree_p['elems']

    data_p, depth_p = pd.DataFrame(), []

    for k,m in enumerate(df_p['NodeName'].unique()):
        subset1 = df_p[df_p['NodeName'] == m]
        subset1.reset_index(drop=True, inplace=True)

        data = pd.DataFrame()
        for i,j in enumerate(elems_p):
            subset2 = subset1[subset1[main_p] == j]
            subset2.reset_index(drop=True, inplace=True)

            if i==0:
                data = pd.concat([data, subset2.drop([main_p], axis=1)], axis=1)
            else:
                data = pd.concat([data, subset2.drop([main_p, 'NodeName'], axis=1)], axis=1)
        data_p = data_p.append(np.round(data,3))
        depth_p.append(data.shape[0])

    data_p.loc[data_p['NodeName'].duplicated(), 'NodeName'] = np.nan
    return data_p, depth_p

def setup_m_data(df_m):
    main_m = tree_m['main'][0]
    elems_m = tree_m['elems']

    data_m, depth_m = pd.DataFrame(), []

    for k,m in enumerate(df_m['NodeName'].unique()):
        subset1 = df_m[df_m['NodeName'] == m]
        subset1.reset_index(drop=True, inplace=True)

        data = pd.DataFrame()
        for i,j in enumerate(elems_m):
            subset2 = subset1[subset1[main_m] == j]
            subset2.reset_index(drop=True, inplace=True)

            if i==0:
                data = pd.concat([data, subset2.drop([main_m], axis=1)], axis=1)
            else:
                data = pd.concat([data, subset2.drop([main_m, 'NodeName'], axis=1)], axis=1)
        data_m = data_m.append(np.round(data,3))
        depth_m.append(data.shape[0])

    data_m.loc[data_m['NodeName'].duplicated(), 'NodeName'] = np.nan
    return data_m, depth_m

def create_workbook(data_p, data_m):
    # Load in metric definitions workbook
    wb = load_workbook(file_def)
    ws = wb.active

    # Make sure definitions sheet has specified name
    ws.title = sheet_1

    # Write data to metrics sheet and append to definitions
    wr = pd.ExcelWriter(file_out, engine='openpyxl')
    wr.book = wb

    data_p.to_excel(wr, startrow=start_p[0] + 2, startcol=start_p[1] - 2, index=False, header=False, sheet_name=sheet_2)
    data_m.to_excel(wr, startrow=start_m[0] + 2, startcol=start_m[1] - 2, index=False, header=False, sheet_name=sheet_2)
    return wb