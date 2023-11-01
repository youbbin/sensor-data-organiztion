import pymongo
import pandas as pd
from datetime import datetime, timedelta
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

# MongoDB 연결 설정

client = pymongo.MongoClient(config.get("DB", "mongo_url")) # MongoDB 서버 주소와 포트 설정
db = client[config.get("DB", "mongo_1m_db")] # 사용할 데이터베이스 이름 설정
collection = db[config.get("DB", "mongo_collection")]  # 사용할 컬렉션 이름 설정

# 데이터 가져오기
start_date_kr = datetime(2023, 10, 30, 8, 21, 0)
end_date_kr = datetime(2023, 10, 30, 20, 0, 0)

start_date_utc = start_date_kr - timedelta(hours=9)
end_date_utc = end_date_kr - timedelta(hours=9)

data = list(collection.find({"datetime": {"$gte": start_date_utc, "$lt": end_date_utc}}))

# 데이터 프레임 생성
df = pd.DataFrame(data)

# 시간 간격 설정
df["datetime"] = pd.to_datetime(df["datetime"])
df.set_index("datetime", inplace=True)

df = df.resample(rule='1T').mean()  # 1분 평균으로 샘플링
print(df)
client.close()

client = pymongo.MongoClient(config.get("DB", "mongo_url"))  # MongoDB 서버 주소와 포트 설정
db = client[config.get("DB", "mongo_1s_db")]  # 데이터베이스 이름 설정
collection = db[config.get("DB", "mongo_collection")]  # 컬렉션 이름 설정

# 리샘플링된 데이터를 MongoDB에 저장
df_dict = df.reset_index().to_dict("records")
collection.insert_many(df_dict)
print("저장완료")
client.close()