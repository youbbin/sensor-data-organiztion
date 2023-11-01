import pandas as pd

df_merge = pd.DataFrame()

# df = pd.read_csv(r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\merged_20230815_20230911.csv")
df = pd.read_csv(r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\4. 실험용 데이터\20231017\20231017.csv")
# df = pd.read_excel(r"D:\workspace\WITLAB\sensorless\data\train_data_distance_angle.xlsx", sheet_name='test_data_0412')
df['azimuth_180_diff'] = abs(180-df['azimuth'])
df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3','illum_1']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = 120
df_["y"] = 0
df_["point"] = 1
df_merge = df_


df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_3']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = -120
df_["y"] = 0
df_["point"] = 3

df_merge = pd.concat([df_merge, df_])

df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_4']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = 120
df_["y"] = 120
df_["point"] = 4
df_merge = pd.concat([df_merge, df_])

df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_5']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = 0
df_["y"] = 120
df_["point"] = 5
df_merge = pd.concat([df_merge, df_])

df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_6']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = -120
df_["y"] = 120
df_["point"] = 6
df_merge = pd.concat([df_merge, df_])

df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_7']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = 120
df_["y"] = 240
df_["point"] = 7
df_merge = pd.concat([df_merge, df_])

df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_8']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = 0
df_["y"] = 240
df_["point"] = 8
df_merge = pd.concat([df_merge, df_])

df_ = df[['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum_9']]
df_.columns = ['datetime', 'elevation', 'azimuth_180_diff', 'illum_1', 'illum_2','illum_3', 'illum']
df_["x"] = -120
df_["y"] = 240
df_["point"] = 9

df_merge = pd.concat([df_merge, df_])

df_merge.to_csv(r"D:\#. WITLAB\#. 6공 데이터\#. 날짜별 데이터\4. 실험용 데이터\20231017\test_data_20231017_창측3개버전.csv")
# df_merge.to_csv(r"D:\workspace\WITLAB\sensorless\data\test_data_0412.csv")

print(df_merge)



