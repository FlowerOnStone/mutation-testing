import csv
import os

path_report = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/mutpy testing/report result"
path_csv = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/mutpy testing/report result/report_summarize.csv"
dirs = os.listdir(path_report)
# print(type(dirs))
# print(dirs[0].split(".")[0] + ".csv")

field_csv = ['status', 'AOD', 'AOR', 'ASR', 'BCR', 'COD', 'COI', 'CRP', 'DDL', 'EHD', 'EXS', 'IHD', 'IOD', 'IOP',
             'LCR', 'LOD', 'LOR', 'ROR', 'SCD', 'SCI', 'SIR', 'sum']

status_mutation_2 = {
        0: 'all',
        1: 'killed',
        2: 'survived',
        3: 'incompetent',
        4: 'timeout'
}

columns = [[0 for index in range(0, 21)] for index2 in range(0, 5)]
rows = [{} for index in range(0, 5)]

for list_report in dirs:
    with open(path_report + "/" + list_report) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = -2
        for row in csv_reader:
            line_count += 1
            if line_count == -1:
                continue
            for num_header in range(1, 22):
                columns[line_count][num_header-1] += (int)(row[num_header])

for i in range(0, 5):
    state_line = {
        'status': status_mutation_2[i],
        'AOD': columns[i][0],
        'AOR': columns[i][1],
        'ASR': columns[i][2],
        'BCR': columns[i][3],
        'COD': columns[i][4],
        'COI': columns[i][5],
        'CRP': columns[i][6],
        'DDL': columns[i][7],
        'EHD': columns[i][8],
        'EXS': columns[i][9],
        'IHD': columns[i][10],
        'IOD': columns[i][11],
        'IOP': columns[i][12],
        'LCR': columns[i][13],
        'LOD': columns[i][14],
        'LOR': columns[i][15],
        'ROR': columns[i][16],
        'SCD': columns[i][17],
        'SCI': columns[i][18],
        'SIR': columns[i][19],
        'sum': columns[i][20]
    }
    rows[i] = state_line

with open(path_csv, 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_csv)
    writer.writeheader()
    writer.writerows(rows)