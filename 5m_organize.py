import os
import csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select


# 파일 저장 위치
save_path = r"D:\WITLAB\#. 6공 데이터\#. 날짜별 데이터\3. 5분 평균(20230815~20230824)"

# 태양 방위각, 고도각 크롤링
driver = webdriver.Chrome("chromedriver.exe")
url = "https://gml.noaa.gov/grad/solcalc/"

start_date_str = "2023-08-15"
end_date_str = "2023-08-24"

def getSunInfo(dt):

    h = dt.hour
    m = dt.minute

    elem = driver.find_element(By.XPATH, '//*[@id="hrbox"]')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(h)
    elem.send_keys(Keys.ENTER)
    elem = driver.find_element(By.XPATH, '//*[@id="mnbox"]')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(m)
    elem.send_keys(Keys.ENTER)
    # elem = driver.find_element(By.XPATH, '//*[@id="scbox"]')
    # elem.send_keys(Keys.BACKSPACE)
    # elem.send_keys(Keys.BACKSPACE)
    # elem.send_keys(0)
    # elem.send_keys(Keys.ENTER)
    elem = driver.find_element(By.XPATH, '//*[@id="azbox"]')
    azimuth = elem.get_attribute("value")
    elem = driver.find_element(By.XPATH, '//*[@id="elbox"]')
    elevation = elem.get_attribute("value")
    return {'azimuth': azimuth, 'elevation': elevation}

def setLocation():
    elem = driver.find_element(By.XPATH, '//*[@id="latbox"]')
    elem.clear()
    elem.send_keys("36.851221")

    elem = driver.find_element(By.XPATH, '//*[@id="lngbox"]')
    elem.clear()
    elem.send_keys("127.152924")

    elem = driver.find_element(By.XPATH, '//*[@id="tz"]')

    elem.send_keys("Asia/Seoul")

    elem.send_keys(Keys.ENTER)


def getMonth(m):
    dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    return dict.get(m)


def setDate(dt):
    month = dt.month
    day = dt.day

    # 월
    elem = driver.find_element(By.XPATH, '//*[@id="mosbox"]')
    elem.send_keys(getMonth(month))
    # time.sleep(0.5)

    # 일
    day_str = str(day-1)
    elem = driver.find_element(By.XPATH, '//*[@id="daybox"]')
    select = Select(elem)
    select.select_by_index(day_str)
    time.sleep(0.5)

    # 초는 0으로 고정(분 단위 데이터일 경우)
    elem = driver.find_element(By.XPATH, '//*[@id="scbox"]')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(0)
    elem.send_keys(Keys.ENTER)


# Function to aggregate data at 5-minute intervals and calculate average
def aggregate_5min(data):
    aggregated_data = []
    current_time = datetime.strptime(data[0]["datetime"], "%Y-%m-%d %H:%M:%S")
    interval_data = []

    for row in data:
        row_datetime = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
        if row_datetime < current_time + timedelta(minutes=5):
            interval_data.append(row)
        else:
            # Calculate average and append to aggregated_data
            if interval_data:
                average_values = {}
                for key in interval_data[0]:
                    if key == "datetime":
                        average_values[key] = current_time
                    elif key and (key.startswith("illum_") or key.startswith("cct_")):
                        values = [float(entry[key]) if entry[key] else 0 for entry in interval_data]
                        values = [value for value in values if value != 0]  # Remove empty values
                        if values:
                            average_values[key] = sum(values) / len(values)
                        else:
                            average_values[key] = 0
                sun_info = getSunInfo(row_datetime)
                average_values.update(sun_info)
                aggregated_data.append(average_values)

            # Reset interval_data and move to next interval
            interval_data = [row]
            current_time = current_time + timedelta(minutes=5)

    return aggregated_data

if __name__ == '__main__':

    driver.get(url)
    setLocation()

    # Specify the directory path where the CSV files are stored
    base_directory = r"D:\WITLAB\#. 6공 데이터\#. 날짜별 데이터\1. 1초 간격"

    # Specify the date range (start_date and end_date)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Traverse through folders within the specified date range
    for folder_name in os.listdir(base_directory):
        date_folder_path = os.path.join(base_directory, folder_name)

        # Check if the folder is within the specified date range and is a directory
        folder_date = datetime.strptime(folder_name, "%Y%m%d")
        if start_date <= folder_date <= end_date and os.path.isdir(date_folder_path):
            setDate(folder_date)
            data = []  # List to hold data

            # Traverse through CSV files within the date folder
            for file_name in os.listdir(date_folder_path):
                if file_name.endswith(".csv"):
                    csv_path = os.path.join(date_folder_path, file_name)

                    with open(csv_path, "r") as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            # Add your logic to process each row of data here
                            data.append(row)

            # Aggregate data at 5-minute intervals and calculate average for illum and cct
            agg_5min_data = aggregate_5min(data)

            # Get date from the folder name
            output_date_folder_path = os.path.join(save_path, folder_name)
            os.makedirs(output_date_folder_path, exist_ok=True)

            # Save aggregated data as CSV
            output_path = os.path.join(output_date_folder_path, folder_name+".csv")
            with open(output_path, "w", newline="") as csv_file:
                fieldnames = list(agg_5min_data[0].keys())
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                csv_writer.writeheader()
                for row in agg_5min_data:
                    csv_writer.writerow(row)

    print("Aggregated data saved as CSV.")
