import os
import shutil

TEST_ROOT = r"../cpython-3.7/Lib/test/"
CODE_ROOT = r"../cpython-3.7/Lib"


def used_unittest(filename):
    filename = TEST_ROOT + filename
    input_file = open(filename, "r")
    lines = input_file.readlines()
    input_file.close()
    for line in lines:
        if "unittest" in line:
            return True
    return False


def get_correct_testcase():
    correct_testcase_file = open(os.path.join(TEST_ROOT, "correct_testcase.txt"))
    lines = correct_testcase_file.readlines()
    correct_testcase_file.close()
    correct_testcase = {line.split()[0]: float(line.split()[1]) for line in lines if float(line.split()[1]) <= 1}
    return correct_testcase


def get_test_file():
    correct_testcase = get_correct_testcase()
    test_files = os.listdir(TEST_ROOT)
    test_files = [file_name for file_name in test_files
                  if file_name.startswith("test_") and file_name.endswith(".py") and file_name in correct_testcase]
    code_files = os.listdir(CODE_ROOT)
    code_files = [file_name for file_name in code_files if ".py" in file_name]

    tmp = []
    for test_file in test_files:
        flag = False
        for code_file in code_files:
            if code_file[0:-3] in test_file and used_unittest(test_file):
                flag = True
                break
        if flag:
            tmp.append(test_file)

    test_files = [file_name for file_name in tmp]
    result = {}
    for test_file in test_files:
        for code_file in code_files:
            if "test_" + code_file in test_file:
                if not (code_file in result):
                    result[code_file] = {test_file: correct_testcase[test_file]}
                else:
                    result[code_file][test_file] = correct_testcase[test_file]
    return result


def copy_file(original_path, target_path, filename):
    original_path = os.path.join(original_path, filename)
    target_path = os.path.join(target_path, filename)
    shutil.copy(original_path, target_path)


def get_test_report():
    log_file = open("log.txt", "r")
    test_report = log_file.readline().split()
    log_file.close()
    return test_report


def run_mutpy():
    report = open("report.csv", "w")
    print("filename,all,killed,survived,incompetent,timeout", file=report)
    test_files = get_test_file()
    for code_file in test_files:
        for test_file in test_files[code_file]:
            copy_file(TEST_ROOT, r".", test_file)
            copy_file(CODE_ROOT, r".", code_file)
            print(code_file)
            script = "mut.py --target " + code_file + " --unit-test " + test_file \
                     + " --timeout-factor " + str(test_files[code_file][test_file] + 0.2)
            os.system(script)
            os.system("mv mutpy_running.txt mutpy\\ result/" + test_file[0:-3] + ".txt")
            os.remove(code_file)
            os.remove(test_file)
    report.close()


def run_unittest():
    test_files = get_test_file()
    for code_file in test_files:
        for test_file in test_files[code_file]:
            copy_file(TEST_ROOT, r".", test_file)
            copy_file(CODE_ROOT, r".", code_file)
            print(test_file)
            os.system("python3 -m unittest " + test_file)
            print()
            os.remove(code_file)
            os.remove(test_file)


run_mutpy()
