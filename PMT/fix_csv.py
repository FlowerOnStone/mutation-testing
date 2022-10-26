import pandas as pd
import os

filenames = os.listdir('./')
filenames = [filename for filename in filenames if ".csv" in filename]

for filename in filenames:
    if filename == "report.csv":
        continue
    data = pd.read_csv(filename)
    print(data.head())
    data = data[data.result != "timeout"]
    data = data[data.result != "incompetent"]
    data.to_csv(filename)