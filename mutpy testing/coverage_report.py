import csv


def create_csv(report_file, code_file, csv_file):
    with open(report_file, 'r') as f:
        report_lines = f.readlines()
    with open(code_file, 'r') as f:
        code_lines = f.readlines()
    isCoverage = [1 for index in range(0, len(code_lines) + 1)]
    fields = 0
    report = ""
    for line in report_lines:
        if line.startswith(code_file):
            report = line.split()
            break
    print(report)
    line = 0
    while line < len(report):
        if report[line] == "":
            line = line + 1
            continue
        fields = fields + 1
        if fields < 5:
            line = line + 1
            continue
        string = report[line]
        string = string.replace(",", "")
        if "-" in string:
            start_line, end_line = map(int, string.split("-"))
            for index in range(start_line, end_line + 1):
                isCoverage[index] = 0
        else:
            isCoverage[int(string)] = 0
        line = line + 1

    rows = [{} for index in range(1, len(code_lines) + 1)]
    print(isCoverage)
    for index in range(1, len(code_lines) + 1):
        state_line = {'line': index, 'coverage': isCoverage[index]}
        rows[index - 1] = state_line
    field_csv = ['line', 'coverage']
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)


def add_report(first_file, second_file, destination_file):
    with open(first_file, "r") as f:
        first_lines = f.readlines()
    with open(second_file, "r") as f:
        second_lines = f.readlines()
    assert len(first_lines) == len(second_lines)
    rows = []
    for index in range(1, len(first_lines)):
        first_lines[index] = first_lines[index].replace("\n", "")
        second_lines[index] = second_lines[index].replace("\n", "")
        rows.append({
            "line": index,
            "coverage": int(first_lines[index].split(",")[1]) + int(second_lines[index].split(",")[1])
        })
    field_csv = ['line', 'coverage']
    with open(destination_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)


def marge_report(unittest_file, tests_file, destination_file):
    print(unittest_file,  tests_file, destination_file)
    with open(unittest_file, "r") as f:
        unittest_lines = f.readlines()
    with open(tests_file, "r") as f:
        tests_lines = f.readlines()
    assert len(unittest_lines) == len(tests_lines)
    rows = []
    for index in range(1, len(unittest_lines)):
        unittest_lines[index] = unittest_lines[index].replace("\n", "")
        tests_lines[index] = tests_lines[index].replace("\n", "")
        rows.append({
            "line": index,
            "unittest_coverage": int(unittest_lines[index].split(",")[1]),
            "nun_test_coverage": int(tests_lines[index].split(",")[1])
        })
    field_csv = ['line', "unittest_coverage", "nun_test_coverage"]
    with open(destination_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)
