import re
import sys
import os
import pandas as pd 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))



#if __name__ == "__main__":
from influxdb_client import InfluxDBClient, Point, BucketsService, Bucket, PostBucketRequest, PatchBucketRequest
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

#client = InfluxDBClient.from_config_file("config.ini") #?????

bucket = "columntest"
url = "http://localhost:8086"
token = "pM4K5ajbmvA4Tirzuzr3F1y0OF1KTNc0gsw5LGrZ-aT93y9KmoOgbqyX88aSZ73K27-nDVPwntfgd_W_cM5QJw=="
org_name = "testorg"
client = InfluxDBClient(url= url, token=token, org= org_name)
measurement_name = "coltest"


### Write ------------------------------------------------------------


# BASE_DIR = os.getcwd()
# df_file = "/home/leezy/CLUST_KETI/KETIPreDataIngestion/data_miss_original.csv"
# input_file = os.path.join(BASE_DIR, df_file)
# df = pd.read_csv(df_file, parse_dates=True, index_col ='timedate')


# # https://docs.influxdata.com/influxdb/v2.1/query-data/get-started/query-influxdb/
# # https://influxdb-client.readthedocs.io/en/v1.2.0/usage.html#the-data-could-be-written-as
# # https://github.com/influxdata/influxdb-client-python
# ### Write
# write_client = client.write_api(write_options= ASYNCHRONOUS)
# write_client.write(bucket, record=df, data_frame_measurement_name=measurement_name)
# write_client.__del__()





### Read InfluxDB Data(Flux query) -----------------------------------------------
# 쿼리문 수정해야함
query_client = client.query_api()

query = 'import "date" from(bucket: "'+bucket+'") |> range(start: 0, stop: now()) |> filter(fn: (r) => r._measurement == "'+measurement_name+'") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") |> drop(columns: ["_start", "_stop"])'

# query ='''
# from(bucket: "example")
#   |> range(start: 2021-01-29T00:00:00Z, stop: 2021-06-01T00:00:00Z)
#   |> filter(fn: (r) => r._measurement == "test1")
#   |> filter(fn: (r) => r._field == "co2")
#   |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
#   |> yield(name: "mean")
# '''

# print(query)

# querytest = 'from(bucket:"'+bucket+'")' \
#         '|> range(start: 0, stop: now()) ' \
#         '|> filter(fn: (r) => r._measurement == "'+measurement_name+'")' \
#         '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")' \
#         '|> drop(columns: ["_start", "_stop"])|> limit(n:10, offset: 0)' 

print(type(query))
data_frame = query_client.query_data_frame(query)
print(type(data_frame))
print(data_frame)






### Read Bucket list -------------------------------------------
# buckets_api = client.buckets_api()
# buckets = buckets_api.find_buckets().buckets
# # print("\n".join([f" ---------\n ID: {bucket.id}\n Name: {bucket.name}\n Retention: {bucket.retention_rules}"
# #                   for bucket in buckets]))

# bk_list = []

# for bucket in buckets:
#   bk_list.append(bucket.name)

# print(bk_list)






### Read meaasurements list --------------------------------------------
# query2 ='import "influxdata/influxdb/schema" schema.measurements(bucket: "'+bucket+'")'

# result = client.query_api().query(org=org_name,query=query2)
# results = []
# for table in result:
#   for record in table.records:
#     results.append(record.values["_value"])

# print(results)






### Read field, time, start, stop of specific measurement ---------------------------------
# query_result = client.query_api().query(query=query)
# results = []
# for table in query_result:
#   for record in table.records:
#     #results.append((record.get_measurement(), record.get_field(), record.get_time(), record.get_start(), record.get_stop()))
#     results.append(record.get_field())

# result_set = set(results)
# field_list = list(result_set)
# print(type(field_list))
# print(field_list)

# for i in results:
#   print(i)







query_client.__del__()


client.__del__()
