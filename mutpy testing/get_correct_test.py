import os
import mutpy

TEST_ROOT = r"../cpython-3.7/Lib/test/"

filename_tests = os.listdir(TEST_ROOT)
filename_tests = [filename for filename in filename_tests
                  if filename.startswith("test_") and filename.endswith(".py")]


def get_correct_testcase(path):
    logFile = open(path, "r")
    lines = logFile.readlines()
    lines = [line.replace("\n", "") for line in lines]
    lines = [line for line in lines if line != ""]
    logFile.close()

    start = 0
    result = []
    while start < len(lines):
        end = start + 1
        while end < len(lines) and not (lines[end].startswith("test_") and lines[end].endswith(".py")):
            end += 1
        running_time = 0
        for i in range(start, end):
            if "Ran" in lines[i] and "test" in lines[i] and "in" in lines[i]:
                tokens = lines[i].split(" ")
                token = tokens[4]
                token = token.replace("s", "")
                running_time = float(token)
            if "OK" in lines[i]:
                result.append([lines[start], running_time])
                break
        start = end
    result.sort()
    return result


correct_testcases = get_correct_testcase("log_unittest.txt")
for testcase in correct_testcases:
    print(testcase[0], testcase[1])