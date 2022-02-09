from formattingfunctions import formatcells, formatlines, formatcolumns
from formattingfunctions import formatdecimals, formatpercentages
from intentsettings import *
import numpy as np


def format_workbook(wb, start_p, start_m, tree_p, tree_m, depth_p, depth_m):

    # Specify sheet to write to
    ws = wb[sheet_2]

    prow, pcol = start_p[0], start_p[1]
    mrow, mcol = start_m[0], start_m[1]

    # Format path headers
    header_p = [i for i in tree_p.keys() if 'header' in i]

    for i in range(0, len(header_p)):
        width = int(np.prod([len(tree_p[m]) for m in tree_p.keys() if 'header' in m][i+1:]))

        ntimes = len(tree_p[header_p[i-1]])
        if i == 0: ntimes = 1

        st, en = pcol, pcol + width - 1
        for n in range(0, ntimes):
            for j,k in enumerate(tree_p[header_p[i]]):
                formatcells(ws, (prow+i, st, prow+i, en), k, border, yellow, alignment)
                st, en = st + width, en + width

    # Format metric headers
    header_m = [i for i in tree_m.keys() if 'header' in i]

    colors = [red, green, blue, orange]

    counter = 0
    for i in range(0, len(header_m)):
        width = int(np.prod([len(tree_m[m]) for m in tree_m.keys() if 'header' in m][i+1:]))

        ntimes = len(tree_m[header_m[i-1]])
        if i == 0: ntimes = 1

        st, en = mcol, mcol + width - 1
        for n in range(0, ntimes):
            for j,k in enumerate(tree_m[header_m[i]]):
                formatcells(ws, (mrow+i, st, mrow+i, en), k, border, colors[counter], alignment)
                st, en = st + width, en + width
        counter += 1

    # Format separating lines
    width = np.prod([len(tree_p[m]) for m in tree_p.keys() if 'header' in m])

    for i,j in enumerate(depth_p):
        pos = (start_p[0] + 2) + int(np.sum(depth_p[:i+1]))
        formatlines(ws, (pos, pcol, pos, pcol + width - 1))

    width = np.prod([len(tree_m[m]) for m in tree_m.keys() if 'header' in m])

    for i,j in enumerate(depth_m):
        pos = (start_m[0] + 2) + int(np.sum(depth_m[:i+1]))
        formatlines(ws, (pos, mcol, pos, mcol + width - 1))

    formatdecimals(ws)
    formatpercentages(ws)
    formatcolumns(ws)

    wb.remove(wb[sheet_1])
    wb.save(file_out)