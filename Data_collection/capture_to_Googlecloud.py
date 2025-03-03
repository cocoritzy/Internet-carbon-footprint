import pyshark
import datetime
import time 
import os #to find the import statment 
from google.cloud import storage 
import socket 
from google.cloud import storage 
import getpass as gt
import subprocess
from google.api_core import exceptions
from google.api_core.retry import Retry


#Connect to google cloud
file_to_keys = '/Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/Key_GoogleCloud.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = file_to_keys
storage_client = storage.Client()

#Create new bucket

# user_name = str(user_name)
# bucket_name ='data_collection_'+user_name
# new bucket name
#bucke_name = bucket_name ='data_collection_'+
# bucket = storage_client.bucket(bucket_name)
# bucket.location = 'EUROPE-WEST2' 
# bucket = storage_client.create_bucket(bucket) # returns Bucket object

username = 'test'
bucket_name ='data_collection_'+username
print('start capturing...')
time.sleep(11)

while True:

    
    #ip_address = socket.getfqdn()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    #print(s.getsockname()[0])
    ip_address = str(s.getsockname()[0])
    s.close()
    
    
    for i in range(1):
        
        now = datetime.datetime.now()
        time_string = now. strftime("%Y-%m-%d_%H-%M-%S")
        current_date_and_time_string = str(time_string)
        extension = ".pcap"
        path = "/Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/pcap/"
        name= "packets_"
        file =  path + name + current_date_and_time_string + extension
        capture = pyshark.LiveCapture(interface="en0", output_file= file, bpf_filter='host'+" "+ ip_address)
        capture.sniff(timeout=8)
    
    
    arr = os.listdir(path)
    
    for file in range(0, len(arr)):
        
        file_name = file + 1
        path = "/Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/pcap/"
        path_output = '/Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/csv/'
        input_file = path + arr[file]
        output_file = path_output + arr[file][:-5] +".csv"
        os.path.join(path,arr[file])
        os.system('ndpiReader  -i' +" "+ input_file +" "+ '-C'+" "+ output_file)
        os.remove(path +arr[file])

    time.sleep(3)
    _MY_RETRIABLE_TYPES = [
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,
    #exceptions.ProtocolError,  
    ]

    def is_retryable(exc):
        return isinstance(exc, _MY_RETRIABLE_TYPES)

    my_retry_policy = Retry(predicate=is_retryable)

    my_bucket = storage_client.get_bucket(bucket_name) #connect_timeout sets the maximum time required to establish the connection to the server
    #read_timeout sets the maximum time to wait for a completed response

    def upload_to_bucket(blob_name, file_path, bucket_name):
        '''
        Upload file to a bucket
        : blob_name  (str) - object name
        : file_path (str)
        : bucket_name (str)
        '''
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return blob
    path_output = '/Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/csv/'    
    arr = os.listdir(path_output)
    # print("\n Number of Files to convert  = ", len(arr), "\n")

    ds_store_file_location = path+ '.DS_store'
    if os.path.isfile(ds_store_file_location):
        os.remove(ds_store_file_location)

    for file in range(0, len(arr)):
        
        path = '/Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/csv/'
        file_name = file + 1
        upload_to_bucket('packets/'+arr[file],os.path.join(path,arr[file]),bucket_name)
        os.remove(path_output+arr[file])



