import pandas as pd

df_merge = pd.DataFrame()

# df = pd.read_csv(r"D:\WITLAB\#. 6공 데이터\#. 날짜별 데이터\merged_20230815_20230829.csv")
df = pd.read_excel(r"D:\workspace\WITLAB\sensorless\data\train_data_distance_angle.xlsx", sheet_name='test_data_0412')
df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum1']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = 162.5
df_["y"] = 0
df_["point"] = 1
df_merge = df_


df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum3']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = -162.5
df_["y"] = 0
df_["point"] = 3

df_merge = pd.concat([df_merge, df_])

df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum4']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = 162.5
df_["y"] = 140
df_["point"] = 4
df_merge = pd.concat([df_merge, df_])

df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum5']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = 0
df_["y"] = 140
df_["point"] = 5
df_merge = pd.concat([df_merge, df_])

df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum6']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = -162.5
df_["y"] = 140
df_["point"] = 6
df_merge = pd.concat([df_merge, df_])

df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum7']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = 162.5
df_["y"] = 280
df_["point"] = 7
df_merge = pd.concat([df_merge, df_])

df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum8']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = 0
df_["y"] = 280
df_["point"] = 8
df_merge = pd.concat([df_merge, df_])

df_ = df[['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum9']]
df_.columns = ['Datetime', 'elevation', 'azimuth_180_diff', 'illum2', 'illum']
df_["x"] = -162.5
df_["y"] = 280
df_["point"] = 9

df_merge = pd.concat([df_merge, df_])

# df_merge.to_csv("D:\\WITLAB\\#. 6공 데이터\\#. 날짜별 데이터\\train_data_20230830.csv")
df_merge.to_csv(r"D:\workspace\WITLAB\sensorless\data\test_data_0412.csv")

print(df_merge)



