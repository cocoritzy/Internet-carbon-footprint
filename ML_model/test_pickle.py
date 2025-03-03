import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

import socket, struct

import imblearn
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import LabelEncoder
from collections import Counter
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import make_pipeline
from imblearn.under_sampling import NearMiss
from sklearn.preprocessing import OneHotEncoder
import sys
import pickle 



filepath = '/Users/colineritz/Desktop/csv/merge_all_users_experience.csv'
df = pd.read_csv(filepath) 
df

#feats = [x for x in df_prediction.columns if x != 'ProtocolName'] #remove protocol name columns to create the input
feats= [ 'src_ip', 'src_port', 'dst_port', 'ndpi_proto', 'server_name_sni',
       'c_to_s_bytes', 'c_to_s_goodput_bytes', 's_to_c_bytes',
       's_to_c_goodput_bytes', 'c_to_s_goodput_ratio', 's_to_c_goodput_ratio',
       'pktlen_c_to_s_min', 'pktlen_c_to_s_avg', 'pktlen_c_to_s_max',
       'pktlen_s_to_c_min', 'pktlen_s_to_c_avg', 'pktlen_s_to_c_max',
       'c_to_s_bytes', 's_to_c_bytes', 'duration']

df = df[feats]

def ip2int(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

# Converting IP addresses into numbers
df['src_ip'] = df['src_ip'].apply(ip2int)

df.isnull().values.any()
df = df.replace(r'^\s*$', np.nan, regex=True)
df['ndpi_proto'] = df['ndpi_proto'].replace(np.nan, 'empty')
df['server_name_sni'] = df['server_name_sni'].replace(np.nan, 'empty')

path = '/Users/colineritz/Desktop/pcap_labelled/proto_number.csv'
df_proto = pd.read_csv(path,on_bad_lines='skip')
key_list = list(df['ndpi_proto'])
dict_lookup = dict(zip(df_proto['ndpi_proto'], df_proto['Number']))
df['ndpi_proto'] =[dict_lookup[item] for item in key_list]
df['ndpi_proto'] = df['ndpi_proto'].apply(np.int64)


path = '/Users/colineritz/Desktop/pcap_labelled/server_number.csv'
df_server = pd.read_csv(path,on_bad_lines='skip')
key_list = list(df['server_name_sni'])
dict_lookup = dict(zip(df_server['server_name_sni'], df_server['number']))
df['server_name_sni'] =[dict_lookup[item] for item in key_list]
df['server_name_sni'] = df['server_name_sni'].apply(np.int64)

df.dropna(inplace=True)
df.isnull().values.any()
print(df.dtypes)
#### Run the ML model
filename = '/Users/colineritz/Desktop/Master_project/data_system/data_system_full/train-model/3_train_model_with_data/finalized_model_n1.sav'
loaded_model = pickle.load(open(filename, 'rb')) #Pickle is a useful Python tool that allows you to save your models
df['Label'] = loaded_model.predict(df)
print(df)
df.to_csv('ML_test_experience.csv', index=False)