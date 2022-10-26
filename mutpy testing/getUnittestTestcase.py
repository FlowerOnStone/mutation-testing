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


filename_tests = os.listdir(TEST_ROOT)
filename_tests = [filename for filename in filename_tests if filename.startswith("test_") and filename.endswith(".py")]
print(len(filename_tests))

filename_codes = os.listdir(CODE_ROOT)
filename_codes = [filename for filename in filename_codes if ".py" in filename]
print(len(filename_codes))

tmp = []
for filename_test in filename_tests:
    flag = False
    for filename_code in filename_codes:
        if filename_code[0:-3] in filename_test:
            flag = True
            break
    if flag:
        tmp.append(filename_test)

filename_tests = [filename for filename in tmp]
tmp = []

for i in range(len(filename_tests)):
    if used_unittest(filename_tests[i]):
        tmp.append(filename_tests[i])

filename_tests = tmp

code_test = {}

for filename_test in filename_tests:
    flag = False
    for filename_code in filename_codes:
        if "test_" + filename_code in filename_test:
            if not (filename_code in code_test):
                code_test[filename_code] = [filename_test]
            else:
                code_test[filename_code].append(filename_test)

for code in code_test:
    for test in code_test[code]:
        original = os.path.join()