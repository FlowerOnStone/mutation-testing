import os
import shutil
import csv
import mutpy_report
import threading

unittest_report_folder = "unittest_report"
mutpy_report_level_one_folder = "mutpy_report_level_one"
mutpy_data_level_one_folder = "mutpy_data_level_one"
mutpy_summary_level_one_folder = "mutpy_summary_level_one"


def get_filenames(code_path, test_path):
    code_files = os.listdir(code_path)
    code_files = [file for file in code_files if file.endswith(".py")]

    test_path_files = os.listdir(test_path)
    test_files = []
    material_files = []
    for file in test_path_files:
        if file.startswith("test_") and file.endswith(".py"):
            test_files.append(file)
        else:
            material_files.append(file)
    code_files.sort()
    test_files.sort()
    material_files.sort()
    return code_files, test_files, material_files


def copy(source_folder, destination_folder, name):
    source = os.path.join(source_folder, name)
    destination = os.path.join(destination_folder, name)
    if os.path.exists(destination):
        return
    if os.path.isdir(source):
        shutil.copytree(source, destination)
    else:
        shutil.copy(source, destination)


def copy_files(source, environment, filenames):
    for filename in filenames:
        copy(source, environment, filename)


def remove_files(environment, names):
    for name in names:
        file_path = os.path.join(environment, name)
        if not os.path.exists(file_path):
            continue
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)


def used_unittest(filename):
    input_file = open(filename, "r")
    try:
        lines = input_file.readlines()
    except:
        return False
    input_file.close()
    for line in lines:
        if "unittest" in line:
            return True
    return False


def run_unittest(filename):
    if os.system("timeout 3s python3 -m unittest " + filename + " 2> unittest_report.txt") != 0:
        return False, 0, 0
    file = open("unittest_report.txt", "r")
    lines = file.readlines()
    file.close()
    test_status = False
    num_test = 0
    running_time = 0.0
    for line in lines:
        if "Ran" in line and "test" in line and "in" in line:
            tokens = line.split(" ")
            num_test = int(tokens[1])
            token = tokens[4]
            token = token.replace("s", "")
            running_time = float(token)
        if "OK" in line:
            test_status = True
            break
    return test_status, num_test, running_time


def get_correct_testcase(code_files, test_files):
    def run_test(test_file):
        print("run test", test_file)
        test_status, num_test, running_time = run_unittest(test_file)
        if test_status and running_time <= 2 and num_test > 0:
            correct_test_files[test_file] = running_time
            test_summary.append({
                'filename': test_file,
                "num_test": num_test,
                "running_time": running_time
            })
    correct_test_files = {}
    test_summary = []
    for test_file in test_files:
        if used_unittest(test_file):
            run_test(test_file)
    field_csv = ["filename", "num_test", "running_time"]
    with open("test_summary.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(test_summary)
    correct_testcase = {}
    for test_file in correct_test_files:
        for code_file in code_files:
            if "test_" + code_file in test_file:
                if not (code_file in correct_testcase):
                    correct_testcase[code_file] = {test_file: correct_test_files[test_file]}
                else:
                    correct_testcase[code_file][test_file] = correct_test_files[test_file]
    for code_file in correct_testcase:
        print(code_file, correct_testcase[code_file])
    return correct_testcase


def run_mutpy_level_one(testcases):
    def run_test(code_file, test_file, log_file, summary_file):
        script = "mut.py --target " + code_file \
                 + " --unit-test " + test_file \
                 + " --report-text " + os.path.join(mutpy_report_level_one_folder, log_file) \
                 + " --summary-data " + os.path.join(mutpy_data_level_one_folder, summary_file) \
                 + " --experimental-operators --timeout-factor " + str(testcases[code_file][test_file] + 0.1)
        os.system(script)
        if not mutpy_report.check_correct(os.path.join(mutpy_report_level_one_folder, log_file)):
            return
        summary = mutpy_report.get_summary(os.path.join(mutpy_report_level_one_folder, log_file))
        summary["filename"] = code_file
        rows.append(summary)
        mutpy_report.report_mutation_level_one(os.path.join(mutpy_report_level_one_folder, log_file),
                                               os.path.join(mutpy_summary_level_one_folder, summary_file))

    if not os.path.exists(mutpy_report_level_one_folder):
        os.makedirs(mutpy_report_level_one_folder)
    if not os.path.exists(mutpy_summary_level_one_folder):
        os.makedirs(mutpy_summary_level_one_folder)
    if not os.path.exists(mutpy_data_level_one_folder):
        os.makedirs(mutpy_data_level_one_folder)
    rows = []
    for code_file in testcases:
        for test_file in testcases[code_file]:
            log_file = code_file[0:-3] + ".txt"
            summary_file = code_file[0:-3] + ".csv"
            run_test(code_file, test_file, log_file, summary_file)
    field_csv = ["filename", "all", "survived", "incompetent", "timeout"]
    with open("mutation_level_one.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)
    mutpy_report.merge_report(mutpy_summary_level_one_folder,
                              os.path.join(mutpy_summary_level_one_folder, "level_one_summary.csv"))


def build_data(code_folder, test_folder, environment):
    code_files, test_files, material_files = get_filenames(code_folder, test_folder)
    copy_files(test_folder, environment, material_files)
    copy_files(test_folder, environment, test_files)
    copy_files(code_folder, environment, code_files)
    testcases = get_correct_testcase(code_files, test_files)
    run_mutpy_level_one(testcases)
    remove_files(environment, code_files)
    remove_files(environment, test_files)
    remove_files(environment, material_files)
    os.system("rm -rf @*")


test_folder = r"../cpython-3.7/Lib/test/"
code_folder = r"../cpython-3.7/Lib"
environment = r"."

build_data(code_folder, test_folder, environment)