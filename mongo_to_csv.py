import os
import pymongo
import csv
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
from configparser import ConfigParser

'''
 mongodb에서 데이터 가져와서 날짜별 폴더 생성 후 csv 파일로 저장
'''
config = ConfigParser()
config.read('config.ini')

# mongodb
mongo_url = config.get("DB", "mongo_url")
# 1분 간격
mongo_db = config.get("DB", "mongo_1m_db")

# 1초 간격
# mongo_db = config.get("DB", "mongo_1s_db")

mongo_collection = config.get("DB", "mongo_collection")

# 파일 저장 경로
base_directory = r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\2. 1분 평균(20230826~)"
# base_directory = r"D:\WITLAB\#. 6공 데이터\#. 날짜별 데이터\1. 1초 간격"
# base_directory = r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\4. 실험용 데이터"

# 태양 방위각, 고도각 크롤링
driver = webdriver.Chrome("chromedriver.exe")
url = "https://gml.noaa.gov/grad/solcalc/"


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


def getSunrise(date):
    date_ = date.strftime("%Y%m%d")
    service_key = config.get("API", "service_key")
    url = config.get("API", "url")
    params = {'serviceKey': service_key, 'locdate': date_, 'location': config.get("API", "location")}

    response = requests.get(url, params=params)
    time.sleep(1)
    root = ET.fromstring(response.text)

    for sr in root.iter('sunrise'):
        sunrise_str = sr.text.strip()
        sunrise_time = datetime.strptime(sunrise_str, "%H%M").time()
        sunrise_datetime = datetime.combine(date, sunrise_time)
        print(date,"의 일출 시간 가져오기 >> ", sunrise_datetime, sep='')
        return sunrise_datetime


def getSunset(date):
    date_ = date.strftime("%Y%m%d")
    service_key = config.get("API", "service_key")
    url = config.get("API", "url")
    params = {'serviceKey': service_key, 'locdate': date_, 'location': config.get("API", "location")}

    response = requests.get(url, params=params)
    time.sleep(1)
    root = ET.fromstring(response.text)

    for ss in root.iter('sunset'):
        sunset_str = ss.text.strip()
        sunset_time = datetime.strptime(sunset_str, "%H%M").time()
        sunset_datetime = datetime.combine(date, sunset_time)
        print(date,"의 일몰 시간 가져오기 >> ", sunset_datetime, sep='')
        return sunset_datetime


if __name__ == '__main__':

    # MongoDB 연결
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db[mongo_collection]

    # 날짜 입력 받기
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    print("-----------------------------------------------")

    driver.get(url)
    setLocation()

    # Convert Korean time to UTC (ISO format)
    start_date_kr = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date_kr = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)  # Include end date by adding one day


    start_date_utc = start_date_kr - timedelta(hours=9)
    end_date_utc = end_date_kr - timedelta(hours=9)

    # Retrieve data between start and end dates
    query = {
        "datetime": {"$gte": start_date_utc, "$lt": end_date_utc}
    }

    data = collection.find(query)


    # 날짜별로 정리
    data_by_date = {}  # Dictionary to hold data by date

    sunrise = datetime(2023,1,1)
    sunset = datetime(2023,1,1)


    for entry in data:

        date_time_iso = entry["datetime"]
        # iso 시간 -> 한국 시간
        date_time_kr = date_time_iso + timedelta(hours=9)
        date_key = date_time_kr.date()
        # print(date_key)

        if date_key not in data_by_date:
            data_by_date[date_key] = []
            sunrise = getSunrise(date_key)
            sunset = getSunset(date_key)
            setDate(date_time_kr)
            print(date_time_kr.date(), "의 데이터 수집 중 ...", sep='')


        if (sunrise + timedelta(minutes=10)) <= date_time_kr <= (sunset - timedelta(minutes=10)):
            sun_info = getSunInfo(date_time_kr)
            entry.update(sun_info)
            data_by_date[date_key].append(entry)

    print("데이터 수집 완료")
    print("-----------------------------------------------")

    # 날짜별 폴더 생성 후 csv 파일 저장
    for date, data_list in data_by_date.items():
        folder_name = date.strftime('%Y%m%d')
        folder_path = os.path.join(base_directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        csv_filename = os.path.join(folder_path, f"{folder_name}.csv")

        with open(csv_filename, "w", newline="") as csv_file:
            if data_list:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(data_list[0].keys())  # Write header

                for entry in data_list:
                    entry["datetime"] = entry["datetime"] + timedelta(hours=9)
                    csv_writer.writerow(entry.values())

                print(f"{date} >> csv 파일 생성 완료")
            else:
                print(f"No relevant data for {date}.")

    print("정리 완료")
