import os
import csv


save_directory = r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터"

# Specify the directory paths where the CSV files are stored
base_directory_1 = r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\2. 1분 평균(20230826~)"
base_directory_2 = r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\3. 5분 평균(20230815~20230824)"

# Specify the output path for the merged illum CSV file
output_illum_csv_path = os.path.join(save_directory, "merged_20230815_20230913.csv")

# Initialize the header for the merged illum CSV
merged_illum_header = ["datetime", "illum_1", "illum_2", "illum_3", "illum_4", "illum_5", "illum_6", "illum_7", "illum_8", "illum_9", "azimuth", "elevation"]

# Initialize the merged illum data list
merged_illum_data = [merged_illum_header]

# Function to extract illum values from a row dictionary
def extract_values(row):
    illum_values = [row[f"illum_{i}"] for i in range(1, 10)]
    azimuth = row["azimuth"]
    elevation = row["elevation"]
    return illum_values + [azimuth, elevation]

# Traverse through both base directories

for base_directory in [base_directory_1, base_directory_2]:
    for folder_name in os.listdir(base_directory):
        date_folder_path = os.path.join(base_directory, folder_name)
        print(folder_name)
        # Check if the folder is a directory
        if os.path.isdir(date_folder_path):
            # Traverse through CSV files within the date folder
            for file_name in os.listdir(date_folder_path):
                if file_name.endswith(".csv"):
                    csv_path = os.path.join(date_folder_path, file_name)

                    with open(csv_path, "r") as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            # Create a row for the merged illum CSV with the desired columns
                            merged_illum_row = [row["datetime"]] + extract_values(row)
                            merged_illum_data.append(merged_illum_row)

# Write the merged illum data to the output CSV file
with open(output_illum_csv_path, "w", newline="") as output_illum_csv_file:
    csv_writer = csv.writer(output_illum_csv_file)
    csv_writer.writerows(merged_illum_data)

print("Merged illum data saved as CSV:", output_illum_csv_path)
