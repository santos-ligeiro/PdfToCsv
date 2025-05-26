import pandas as pd
import os
import re
import sys
import subprocess

# Check if the folder path is provided as a command-line argument
if len(sys.argv) > 1:
    pdf_folders = sys.argv[1]
else:
    print("Please provide the folder path as a command-line argument.")
    sys.exit(1)
csv_folder = "./csv"

print("Converting from pdf to csv.")
# stream = os.popen('./pdf_to_csv.sh '+pdf_folders+' '+csv_folder)
# output = stream.read()

process = subprocess.Popen(['./pdf_to_csv.sh', pdf_folders, csv_folder], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    print(output.strip())

    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip())
        break


print("Converted from pdf to csv.")

# Get the paths of all files in the folder
file_paths = []
for root, dirs, files in os.walk(csv_folder):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)

cc = pd.DataFrame()

# create row headers in the dataframe
cc['header'] = pd.read_csv(file_paths[0], header=None)[0][19:46]

headers = pd.read_csv(file_paths[0], header=None)[0][19:46].to_list()
headers = ['Animal', 'Date'] + headers
alt = pd.DataFrame(columns=headers)

print("Processing csv data.")
# insert the column per csv file
for path in file_paths:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(path, header=None)
    
    animalCell = df[0][8]
    animal = re.findall(r'\d+', animalCell)[-1]
    animal = int(animal)

    dateCell = df[3][3]
    # Extract the date from the dateCell
    date_match = re.search(r'\d{2}/\d{2}/\d{4}', dateCell)
    if date_match:
        date = date_match.group(0)
    else:
        print("Date not found in the expected format.")
        continue

    # check if reticulicitos cell has value if not correct the columns
    match = re.search(r'(\d+,\d+|\d+)', df[1][38])
    if not match:
        print("Correcting reticulicitos.")
        for i, row in enumerate(df[1][38:47]):
            df[1][38+i] = df[1][38+i+1]

    data = df[1][19:46]
    # print(data)
    numbers = []
    for item in data:
        if pd.notnull(item):  # Check if the item is not NaN
            match = re.findall(r'(\d+,\d+|\d+)', item)
            if match:
                number = float(match[-1].replace(',', '.'))
                numbers.append(number)
            else:
                numbers.append(item)
        else:
            numbers.append(item)

    cc[animal] = numbers

    new_row = [animal, date] + numbers
    alt = pd.concat([alt, pd.DataFrame([new_row], columns=headers)], ignore_index=True) 

print("Data processed.")

cc.to_csv("./data.csv")

alt['Animal'] = pd.Categorical(alt['Animal'], [16, 23, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22])
alt = alt.sort_values(by='Animal')
alt.to_csv("./data_alt.csv", index=False)

print("Data saved to data.csv")