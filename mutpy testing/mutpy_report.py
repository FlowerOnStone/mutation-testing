import csv
import os


def check_correct(file_path):
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()
    return "passed" in lines[3]

def get_summary(file_path):
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()
    result = {}
    for index in range(len(lines) - 5, len(lines) - 1):
        tokens = lines[index].split()
        tokens[1] = tokens[1].replace(":", "")
        result[tokens[1]] = int(tokens[2])
    return result


mutation_names = ['AOD', 'AOR', 'ASR', 'BCR', 'COD', 'COI', 'CRP', 'DDL', 'EHD', 'EXS', 'IHD', 'IOD', 'IOP', 'LCR',
                  'LOD', 'LOR', 'ROR', 'SCD', 'SCI', 'SIR', 'CDI', 'OIL', 'RIL', 'SDI', 'SDL', 'SVD', "ZIL", 'sum']
field_csv = ['status', 'AOD', 'AOR', 'ASR', 'BCR', 'COD', 'COI', 'CRP', 'DDL', 'EHD', 'EXS', 'IHD', 'IOD', 'IOP',
             'LCR', 'LOD', 'LOR', 'ROR', 'SCD', 'SCI', 'SIR', 'CDI', 'OIL', 'RIL', 'SDI', 'SDL', 'SVD', "ZIL", 'sum']


def report_mutation_level_one(report_file, summary_file):
    file_report = open(report_file, 'r')
    lines = file_report.readlines()
    file_report.close()

    num_mutation_each_type = {
        mutation_name: 0 for mutation_name in mutation_names
    }
    num_killed_mutation_each_type = {
        mutation_name: 0 for mutation_name in mutation_names
    }
    num_survived_mutation_each_type = {
        mutation_name: 0 for mutation_name in mutation_names
    }
    num_incompetent_mutation_each_type = {
        mutation_name: 0 for mutation_name in mutation_names
    }
    num_timeout_mutation_each_type = {
        mutation_name: 0 for mutation_name in mutation_names
    }

    status_mutation = {
        'killed': 0,
        'survived\n': 1,
        'incompetent\n': 2,
        'timeout\n': 3
    }

    status_mutation_2 = {
        0: 'all',
        1: 'killed',
        2: 'survived',
        3: 'incompetent',
        4: 'timeout'
    }

    for i in range(6, len(lines)):
        list_elements = lines[i].split(" ")
        mutation = ""
        status = ""
        for element in list_elements:
            if element in num_mutation_each_type:
                mutation = element
            elif element in status_mutation:
                status = element.split('\n')[0]
                break
        if mutation == "":
            break
        num_mutation_each_type[mutation] += 1
        num_mutation_each_type['sum'] += 1
        if status == 'killed':
            num_killed_mutation_each_type[mutation] += 1
            num_killed_mutation_each_type['sum'] += 1
        elif status == 'survived':
            num_survived_mutation_each_type[mutation] += 1
            num_survived_mutation_each_type['sum'] += 1
        elif status == 'timeout':
            num_timeout_mutation_each_type[mutation] += 1
            num_timeout_mutation_each_type['sum'] += 1
        else:
            num_incompetent_mutation_each_type[mutation] += 1
            num_incompetent_mutation_each_type['sum'] += 1

    list_dict = [num_mutation_each_type, num_killed_mutation_each_type, num_survived_mutation_each_type,
                 num_incompetent_mutation_each_type, num_timeout_mutation_each_type]

    rows = [{} for index in range(0, 5)]

    for i in range(0, 5):
        state_line = {
            mutation: list_dict[i][mutation] for mutation in mutation_names
        }
        state_line['status'] = status_mutation_2[i]
        rows[i] = state_line

    with open(summary_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)


def merge_report(path_report, path_result):
    dirs = os.listdir(path_report)
    # print(type(dirs))
    # print(dirs[0].split(".")[0] + ".csv")

    status_mutation_2 = {
        0: 'all',
        1: 'killed',
        2: 'survived',
        3: 'incompetent',
        4: 'timeout'
    }

    columns = [{mutation_name: 0 for mutation_name in mutation_names} for index2 in range(0, 5)]
    rows = [{} for index in range(0, 5)]

    for list_report in dirs:
        with open(path_report + "/" + list_report) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = -2
            for row in csv_reader:
                line_count += 1
                if line_count == -1:
                    continue
                for mutation_name in mutation_names:
                    columns[line_count][mutation_name] += int(row[mutation_name])

    for i in range(0, 5):
        state_line = {mutation_name: columns[i][mutation_name] for mutation_name in mutation_names}
        state_line['status'] = status_mutation_2[i]
        rows[i] = state_line

    with open(path_result, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)
