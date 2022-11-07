import csv
import os


path_report = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/mutpy testing/mutpy result"
path_csv = "/Users/nguyenngocanh/Desktop/mutpy/mutation-testing/mutpy testing/report result/report_mutation_level1_"

list_file_report_test = os.listdir(path_report)

for file_test in list_file_report_test:
    file_report = open(path_report + "/" + file_test, 'r')
    file_report = file_report.readlines()

    num_mutation_each_type = {
        'AOD': 0,
        'AOR': 0,
        'ASR': 0,
        'BCR': 0,
        'COD': 0,
        'COI': 0,
        'CRP': 0,
        'DDL': 0,
        'EHD': 0,
        'EXS': 0,
        'IHD': 0,
        'IOD': 0,
        'IOP': 0,
        'LCR': 0,
        'LOD': 0,
        'LOR': 0,
        'ROR': 0,
        'SCD': 0,
        'SCI': 0,
        'SIR': 0,
        'sum': 0
    }
    num_killed_mutation_each_type = {
        'AOD': 0,
        'AOR': 0,
        'ASR': 0,
        'BCR': 0,
        'COD': 0,
        'COI': 0,
        'CRP': 0,
        'DDL': 0,
        'EHD': 0,
        'EXS': 0,
        'IHD': 0,
        'IOD': 0,
        'IOP': 0,
        'LCR': 0,
        'LOD': 0,
        'LOR': 0,
        'ROR': 0,
        'SCD': 0,
        'SCI': 0,
        'SIR': 0,
        'sum': 0
    }
    num_survived_mutation_each_type = {
        'AOD': 0,
        'AOR': 0,
        'ASR': 0,
        'BCR': 0,
        'COD': 0,
        'COI': 0,
        'CRP': 0,
        'DDL': 0,
        'EHD': 0,
        'EXS': 0,
        'IHD': 0,
        'IOD': 0,
        'IOP': 0,
        'LCR': 0,
        'LOD': 0,
        'LOR': 0,
        'ROR': 0,
        'SCD': 0,
        'SCI': 0,
        'SIR': 0,
        'sum': 0
    }
    num_incompetent_mutation_each_type = {
        'AOD': 0,
        'AOR': 0,
        'ASR': 0,
        'BCR': 0,
        'COD': 0,
        'COI': 0,
        'CRP': 0,
        'DDL': 0,
        'EHD': 0,
        'EXS': 0,
        'IHD': 0,
        'IOD': 0,
        'IOP': 0,
        'LCR': 0,
        'LOD': 0,
        'LOR': 0,
        'ROR': 0,
        'SCD': 0,
        'SCI': 0,
        'SIR': 0,
        'sum': 0
    }
    num_timeout_mutation_each_type = {
        'AOD': 0,
        'AOR': 0,
        'ASR': 0,
        'BCR': 0,
        'COD': 0,
        'COI': 0,
        'CRP': 0,
        'DDL': 0,
        'EHD': 0,
        'EXS': 0,
        'IHD': 0,
        'IOD': 0,
        'IOP': 0,
        'LCR': 0,
        'LOD': 0,
        'LOR': 0,
        'ROR': 0,
        'SCD': 0,
        'SCI': 0,
        'SIR': 0,
        'sum': 0
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

    type_mutation = {
        0: 'AOD',
        1: 'AOR',
        2: 'ASR',
        3: 'BCR',
        4: 'COD',
        5: 'COI',
        6: 'CRP',
        7: 'DDL',
        8: 'EHD',
        9: 'EXS',
        10: 'IHD',
        11: 'IOD',
        12: 'IOP',
        13: 'LCR',
        14: 'LOD',
        15: 'LOR',
        16: 'ROR',
        17: 'SCD',
        18: 'SCI',
        19: 'SIR'
    }

    for i in range(6, len(file_report)):
        list_elements = file_report[i].split(" ")
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

    field_csv = ['status', 'AOD', 'AOR', 'ASR', 'BCR', 'COD', 'COI', 'CRP', 'DDL', 'EHD', 'EXS', 'IHD', 'IOD', 'IOP',
                 'LCR', 'LOD', 'LOR', 'ROR', 'SCD', 'SCI', 'SIR', 'sum']
    rows = [{} for index in range(0, 5)]

    for i in range(0, 5):
        state_line = {
            'status': status_mutation_2[i],
            'AOD': list_dict[i]['AOD'],
            'AOR': list_dict[i]['AOR'],
            'ASR': list_dict[i]['ASR'],
            'BCR': list_dict[i]['BCR'],
            'COD': list_dict[i]['COD'],
            'COI': list_dict[i]['COI'],
            'CRP': list_dict[i]['CRP'],
            'DDL': list_dict[i]['DDL'],
            'EHD': list_dict[i]['EHD'],
            'EXS': list_dict[i]['EXS'],
            'IHD': list_dict[i]['IHD'],
            'IOD': list_dict[i]['IOD'],
            'IOP': list_dict[i]['IOP'],
            'LCR': list_dict[i]['LCR'],
            'LOD': list_dict[i]['LOD'],
            'LOR': list_dict[i]['LOR'],
            'ROR': list_dict[i]['ROR'],
            'SCD': list_dict[i]['SCD'],
            'SCI': list_dict[i]['SCI'],
            'SIR': list_dict[i]['SIR'],
            'sum': list_dict[i]['sum']
        }
        rows[i] = state_line

    file_csv = path_csv + file_test.split(".")[0] + ".csv"
    with open(file_csv, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)
