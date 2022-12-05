import os
import shutil
import csv
import mutpy_report
import coverage_report
from multiprocessing import Pool
import unittest
from sklearn.model_selection import train_test_split
import pandas as pd


unittest_report_folder = "unittest_report"
level_one_report = "level_one_report"
level_one_data = "level_one_data"
level_one_summary = "level_one_summary"
level_two_report = "level_two_report"
level_two_data = "level_two_data"
coverage_report_folder = "coverage_report"
coverage_summary_folder = "coverage_summary"
data_folder = "data"
data_level_one = os.path.join(data_folder, "level_one")
data_level_two = os.path.join(data_folder, "level_two")

ignore = ["pstats.py", "turtle.py", "sysconfig.py"]

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
        if name == "data":
            continue
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
    report_file = os.path.join(unittest_report_folder, filename[0:-2] + "txt")
    if os.system("timeout 2s python3 -m unittest " + filename + " 2> " + report_file + " >/dev/null") != 0:
        return filename, False, 0, 0
    with open(report_file, "r") as f:
        lines = f.readlines()
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
    print(filename, test_status)
    return filename, test_status, num_test, running_time


def get_correct_testcase(code_files, test_files):
    correct_test_files = {}
    test_summary = []
    tmp = []
    for test_file in test_files:
        if used_unittest(test_file):
            tmp.append(test_file)
    create_folder(unittest_report_folder)
    with Pool(processes=4) as pool:
        result = pool.map(run_unittest, tmp)
    for x in result:
        if x[1]:
            test_summary.append({
                "filename": x[0],
                "num_test": x[2],
                "running_time": x[3]})
            correct_test_files[x[0]] = x[3]
    field_csv = ["filename", "num_test", "running_time"]
    with open("test_summary.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(test_summary)
    correct_testcase = {}
    for test_file in correct_test_files:
        for code_file in code_files:
            if code_file in ignore:
                continue
            if "test_" + code_file in test_file:
                if not (code_file in correct_testcase):
                    correct_testcase[code_file] = {test_file: correct_test_files[test_file]}
                else:
                    correct_testcase[code_file][test_file] = correct_test_files[test_file]
    return correct_testcase


def create_folder(folder_name):
    if folder_name and not os.path.exists(folder_name):
        os.makedirs(folder_name)


def run_mutpy(code_file, test_file, time_limit, level, report_folder, data_folder, summary_folder):
    name = test_file[0:-3]
    report_file = os.path.join(report_folder, name + ".txt")
    data_file = os.path.join(data_folder, name + ".csv")
    if os.path.exists(data_file):
        if not mutpy_report.check_correct(report_file):
            return {
                "filename": code_file,
                "all": 0,
                "killed": 0,
                "survived": 0,
                "incompetent": 0,
                "timeout": 0
            }
        if level == 1:
            summary_file = os.path.join(summary_folder, name + ".csv")
            mutpy_report.report_mutation_level_one(report_file, summary_file)

        summary = mutpy_report.get_summary(report_file)
        summary["filename"] = code_file
        return summary
    script = "mut.py --target " + code_file \
             + " --unit-test " + test_file \
             + " --report-text " + report_file \
             + " --summary-data " + data_file \
             + " --timeout-factor " + str(time_limit) \
             + " --experimental-operators --disable-stdout"
    if level == 2:
        script += " --order 2 --hom-strategy ALL_PAIR"
    script += " > /dev/null"
    print(script)
    os.system(script)
    print("end ", code_file)
    if not mutpy_report.check_correct(report_file):
        return {
            "filename": code_file,
            "all": 0,
            "killed": 0,
            "survived": 0,
            "incompetent": 0,
            "timeout": 0
            }
    if level == 1:
        summary_file = os.path.join(summary_folder, name + ".csv")
        mutpy_report.report_mutation_level_one(report_file, summary_file)

    summary = mutpy_report.get_summary(report_file)
    summary["filename"] = code_file
    return summary


def mutpy(testcases, level, report_folder, data_folder, summary_folder):
    create_folder(report_folder)
    create_folder(data_folder)
    create_folder(summary_folder)
    args = []
    for code_file in testcases:
        for test_file in testcases[code_file]:
            args.append((code_file, test_file, testcases[code_file][test_file] + 0.1,
                        level, report_folder, data_folder, summary_folder))
    rows = []
    with Pool(processes=8) as pool:
        rows = pool.starmap(run_mutpy, args)
    field_csv = ["filename", "all", "killed", "survived", "incompetent", "timeout"]
    print(level)
    with open("mutation_level_{}.csv".format(level), 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
        writer.writerows(rows)
    if level == 1:
        mutpy_report.merge_summary(summary_folder, os.path.join(summary_folder, "summary.csv"))




def coverage(code_file, test_file):
    def get_test(test_suite, prefix_name):
        result = []
        if isinstance(test_suite, unittest.suite.TestSuite):
            for test in test_suite:
                result.extend(get_test(test, prefix_name))
        elif test_suite.id().startswith(prefix_name):
            result.append(test_suite.id())
        return result

    def run(file, report_file, unittest):
        if os.path.exists(report_file):
            return
        data_file = file[0:-3] + ".coverage"
        script = "coverage run --data-file={} {}".format(data_file, file)
        if unittest:
            script = "coverage run --data-file={} -m unittest {}".format(data_file, file)
        os.system(script)
        os.system("coverage report -m --data-file={} > {}".format(data_file, report_file))
        os.remove(data_file)

    name = test_file[0:-3]
    report_folder = os.path.join(coverage_report_folder, name)
    summary_folder = os.path.join(coverage_summary_folder, name)
    create_folder(report_folder)
    create_folder(summary_folder)
    test_suite = unittest.TestLoader().discover(".", pattern=name + '.py', top_level_dir=None)
    test_name = get_test(test_suite, name)
    report_file = os.path.join(report_folder, name + ".txt")
    summary_file = os.path.join(summary_folder, "unittest.csv")
    run(test_file, report_file, True)
    coverage_report.create_csv(report_file, code_file, summary_file)
    test_coverage = os.path.join(summary_folder, "test_coverage.csv")
    with open(summary_file, "r") as f:
        lines = f.readlines()
        lines = [line.replace("1", "0") for line in lines]
        lines = [line.replace("\n", "") for line in lines]
        with open(test_coverage, "w") as g:
            g.write("\n".join(lines))
    for test in test_name:
        filename = test + ".py"
        with open(filename, "w") as f:
            print("import unittest", file=f)
            print("print(unittest.TextTestRunner().run(test=unittest.TestLoader().loadTestsFromName(\""
                  + test + "\")))", file=f)
        report_file = os.path.join(report_folder, test + ".txt")
        summary_file = os.path.join(summary_folder, test + ".csv")
        run(filename, report_file, False)
        coverage_report.create_csv(report_file, code_file, summary_file)
        coverage_report.add_report(test_coverage, summary_file, test_coverage)
        os.remove(filename)
    coverage_report.marge_report(os.path.join(summary_folder, "unittest.csv"), test_coverage,
                                 os.path.join(coverage_summary_folder, test_file[0:-3] + ".csv"))


def run_coverage(testcases):
    create_folder(coverage_report_folder)
    create_folder(coverage_summary_folder)
    test = []
    for code_file in testcases:
        for test_file in testcases[code_file]:
            test.append((code_file, test_file))
    with Pool(processes=1) as pool:
        pool.starmap(coverage, test)


def build_data():
    def get_test_info():
        result = {}
        with open("test_summary.csv", "r") as f:
            rows = csv.DictReader(f, delimiter=",")
            for row in rows:
                result[row["filename"]] = int(row["num_test"])
        return result

    def load_coverage_data(file):
        result = [{}]
        with open(file, "r") as f:
            rows = csv.DictReader(f, delimiter=",")
            for row in rows:
                row["line"] = int(row["line"])
                row["unittest_coverage"] = int(row["unittest_coverage"])
                row["nun_test_coverage"] = int(row["nun_test_coverage"])
                result.append(row)
        return result

    def get_coverage(start_line, end_line, num_test, coverage_data):
        if start_line >= len(coverage_data):
            return 0.0, 0.0, 0.0, 0.0
        start_line_coverage = coverage_data[start_line]["unittest_coverage"]
        start_line_test_coverage = coverage_data[start_line]["nun_test_coverage"] / num_test
        body_coverage = 0
        body_test_coverage = 0
        end_line = min(end_line, len(coverage_data) - 1)
        for line in range(start_line, end_line + 1):
            body_coverage += coverage_data[line]["unittest_coverage"]
            body_test_coverage += coverage_data[line]["nun_test_coverage"]
        body_coverage = body_coverage / (end_line - start_line + 1)
        body_test_coverage = body_test_coverage / ((end_line - start_line + 1) * num_test)
        return start_line_coverage, start_line_test_coverage, body_coverage, body_test_coverage

    def is_ancestor(mutant_1_line, mutant_1_end_line, mutant_2_line, mutant_2_end_line):
        return (mutant_1_line > mutant_2_line and mutant_1_end_line <= mutant_2_end_line) \
               or (mutant_2_line > mutant_1_line and mutant_2_end_line <= mutant_1_end_line)

    def build_data_level_one(source_data, coverage_data, destination_file, num_test):
        result = []
        with open(source_data, "r") as f:
            rows = csv.DictReader(f, delimiter=",")
            for row in rows:
                result.append(row)
                start_line_coverage, start_line_test_coverage, body_coverage, body_test_coverage = get_coverage(
                    int(row["line"]),
                    int(row["end_line"]),
                    num_test,
                    coverage_data
                )
                row["start_line_coverage"] = start_line_coverage
                row["start_line_test_coverage"] = start_line_test_coverage
                row["body_coverage"] = body_coverage
                row["body_test_coverage"] = body_test_coverage
                result.append(row)
        field_csv = ["id", "depth_on_ast", "type_operator", "type_statement", "type_return", "line", "end_line",
                     "start_line_coverage", "start_line_test_coverage", "body_coverage", "body_test_coverage", "result"]
        with open(destination_file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=field_csv)
            writer.writeheader()
            writer.writerows(result)

    def build_data_level_two(source_data, coverage_data, destination_file, num_test):
        result = []
        with open(source_data, "r") as f:
            rows = csv.DictReader(f, delimiter=",")
            for row in rows:
                for index in range(1, 3):
                    start_line_coverage, start_line_test_coverage, body_coverage, body_test_coverage = get_coverage(
                        int(row["mutant_{}_line".format(index)]),
                        int(row["mutant_{}_end_line".format(index)]),
                        num_test,
                        coverage_data
                    )
                    row["mutant_{}_start_line_coverage".format(index)] = start_line_coverage
                    row["mutant_{}_start_line_test_coverage".format(index)] = start_line_test_coverage
                    row["mutant_{}_body_coverage".format(index)] = body_coverage
                    row["mutant_{}_body_test_coverage".format(index)] = body_test_coverage
                row["ancestor"] = is_ancestor(row["mutant_1_line"], row["mutant_1_end_line"],
                                              row["mutant_2_line"], row["mutant_2_end_line"])
                result.append(row)

        field_csv = ["id", "distance_between_two_mutant", "mutant_1_depth_on_ast", "mutant_1_type_operator",
                     "mutant_1_type_statement", "mutant_1_type_return", "mutant_1_line", "mutant_1_end_line",
                     "mutant_1_start_line_coverage", "mutant_1_start_line_test_coverage",
                     "mutant_1_body_coverage", "mutant_1_body_test_coverage",
                     "mutant_2_depth_on_ast", "mutant_2_type_operator", "mutant_2_type_statement",
                     "mutant_2_type_return", "mutant_2_line", "mutant_2_end_line",
                     "mutant_2_start_line_coverage", "mutant_2_start_line_test_coverage",
                     "mutant_2_body_coverage", "mutant_2_body_test_coverage",
                     "ancestor", "result"]
        with open(destination_file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=field_csv)
            writer.writeheader()
            writer.writerows(result)

    test_info = get_test_info()
    create_folder(data_folder)
    create_folder(data_level_one)
    create_folder(data_level_two)
    for test in test_info:
        name = test[0:-3] + ".csv"
        coverage_file = os.path.join(coverage_summary_folder, name)
        data_l1 = os.path.join(level_one_data, name)
        data_l2 = os.path.join(level_two_data, name)
        if os.path.exists(coverage_file) and os.path.exists(data_l1) and os.path.exists(data_l2):
            print(test)
            coverage_data = load_coverage_data(coverage_file)
            build_data_level_one(data_l1, coverage_data, os.path.join(data_level_one, name), test_info[test])
            build_data_level_two(data_l2, coverage_data, os.path.join(data_level_two, name), test_info[test])

def build(code_folder, test_folder):
    environment = r"."
    code_files, test_files, material_files = get_filenames(code_folder, test_folder)
    copy_files(test_folder, environment, material_files)
    copy_files(test_folder, environment, test_files)
    copy_files(code_folder, environment, code_files)
    testcases = get_correct_testcase(code_files, test_files)
    # mutpy(testcases, 1, level_one_report, level_one_data, level_one_summary)
    # mutpy(testcases, 2, level_two_report, level_two_data, "")
    # run_coverage(testcases)
    build_data()
    remove_files(environment, code_files)
    remove_files(environment, test_files)
    remove_files(environment, material_files)
    os.system("rm -rf @*")


def merge_data(folder):
    filenames = os.listdir(folder)
    filenames.sort()
    id = 0
    data_file = os.path.join(folder, "data.csv")
    field_csv = ["id", "distance_between_two_mutant", "mutant_1_depth_on_ast", "mutant_1_type_operator",
                 "mutant_1_type_statement", "mutant_1_type_return", "mutant_1_line", "mutant_1_end_line",
                 "mutant_1_start_line_coverage", "mutant_1_start_line_test_coverage",
                 "mutant_1_body_coverage", "mutant_1_body_test_coverage",
                 "mutant_2_depth_on_ast", "mutant_2_type_operator", "mutant_2_type_statement",
                 "mutant_2_type_return", "mutant_2_line", "mutant_2_end_line",
                 "mutant_2_start_line_coverage", "mutant_2_start_line_test_coverage",
                 "mutant_2_body_coverage", "mutant_2_body_test_coverage",
                 "ancestor", "result"]
    rows = []
    id = 0
    with open(data_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=field_csv)
        writer.writeheader()
    for filename in filenames:
        if filename == ".DS_Store":
            continue
        print(filename)
        with open(os.path.join(folder, filename), "r") as f:
            tmp = csv.DictReader(f, delimiter=",")
            for row in tmp:
                id += 1
                row["id"] = id
                rows.append(row)
            with open(data_file, "a") as f:
                writer = csv.DictWriter(f, fieldnames=field_csv)
                writer.writerows(rows)
            rows = []


def split_test(folder, filename):
    train_file = "train_" + filename
    test_file = "test_" + filename
    data = pd.read_csv(os.path.join(folder, filename))
    train_data, test_data = train_test_split(data, test_size=0.1)
    train_data.to_csv(os.path.join(folder, train_file), index=False)
    test_data.to_csv(os.path.join(folder, test_file), index=False)


def small_data(folder, filename):
    small_data_file = "small_" + filename
    train_file = "train_small_" + filename
    test_file = "test_small_" + filename
    data = pd.read_csv(os.path.join(folder, filename))
    tmp, small = train_test_split(data, test_size=0.1)
    small.to_csv(os.path.join(folder, small_data_file), index=False)
    train_data, test_data = train_test_split(small, test_size=0.1)
    train_data.to_csv(os.path.join(folder, train_file), index=False)
    test_data.to_csv(os.path.join(folder, test_file), index=False)

code = r"../cpython-3.7/Lib"
test = r"../cpython-3.7/Lib/test/"

small_data(data_level_two, "data.csv")