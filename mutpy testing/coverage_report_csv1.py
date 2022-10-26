import csv

path_report = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/testing/report.txt"
path_file_code = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/testing/"
path_csv1 = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/testing/unittest_cover.csv"

file_report = open(path_report, 'r')
file_report = file_report.readlines()
file_report = file_report[2].split(" ")
path_file_code = path_file_code + file_report[0]
file_code = open(path_file_code, 'r')
file_code = file_code.readlines()

isCoverage = [1 for index in range(0, len(file_code) + 1)]
fields = 0
line = 0
while line < len(file_report):
    if file_report[line] == "":
        line = line + 1
        continue
    fields = fields + 1
    if fields < 5:
        line = line + 1
        continue
    string = file_report[line]
    start_line = 0
    end_line = 0
    isSeparate = False
    for index in range(0, len(string)):
        if string[index] == "," or string[index] == "\n":
            continue
        if string[index] == "-":
            isSeparate = True
            continue
        if isSeparate:
            end_line = end_line * 10 + int(string[index])
        else:
            start_line = start_line * 10 + int(string[index])
    for index in range(start_line, end_line + 1):
        isCoverage[index] = 0
    line = line + 1

field_csv1 = ['line', 'coverage']
rows = [{} for index in range(1, len(file_code) + 1)]

for index in range(1, len(file_code) + 1):
    state_line = {'line': index, 'coverage': isCoverage[index]}
    rows[index - 1] = state_line

with open(path_csv1, 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_csv1)
    writer.writeheader()
    writer.writerows(rows)
