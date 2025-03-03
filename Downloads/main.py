# Import necessary libraries
import os
import time
from datetime import datetime, date, timedelta
import calendar
import numpy as np
import pandas as pd
import requests
import pickle
from google.cloud import storage
from codecarbon import EmissionsTracker

# Initialize the EmissionsTracker to monitor carbon emissions from the script
tracker = EmissionsTracker()
tracker.start()

# Start timing the script execution
t0 = time.time()

# Set Google Cloud credentials and initialize the storage client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/colineritz/Desktop/output/Key_GoogleCloud.json'
storage_client = storage.Client()

# Constants for time-based operations
s1 = '09:30:37'
s2 = '10:59:00'

# Function to find occurrences of a character in a string
def find_occurrences(s, ch):
    """Find all positions of a character in a string."""
    return [i for i, letter in enumerate(s) if letter == ch]

# Function to download files from a Google Cloud Storage bucket
def download_from_bucket(bucket_name, blob_path, local_path):
    """Download files from a Google Cloud Storage bucket to a local directory."""
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    bucket = storage_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=blob_path))

    for blob in blobs:
        if not blob.name.endswith("/"):
            folder_locations = find_occurrences(blob.name.replace(blob_path, ''), '/')
            if folder_locations:
                for folder in folder_locations:
                    create_folder = os.path.join(local_path, blob.name.replace(blob_path, '')[:folder])
                    if not os.path.exists(create_folder):
                        os.makedirs(create_folder)
            download_path = os.path.join(local_path, blob.name.replace(blob_path, ''))
            blob.download_to_filename(download_path)

# Download data from the bucket
local_path = '/Users/colineritz/Desktop/output/download_data/'
download_from_bucket('three_user', 'packets', local_path)

# Filter files for the relevant day
time_string_day = "2022-06-02"
local_dir = '/Users/colineritz/Desktop/output/download_data/'
files = os.listdir(local_dir)

# Merge CSV files for the specified day
data_frames = []
df_merge = pd.DataFrame(data_frames)

for file in files:
    filepath = os.path.join(local_dir, file)
    if time_string_day in filepath:
        df = pd.read_csv(filepath, on_bad_lines='skip')
        time_file = file[12:-4]  # Extract time from filename
        df['Time_5min'] = time_file
        df_merge = df_merge.append(df, ignore_index=True)
        os.remove(filepath)
    else:
        os.remove(filepath)

# Clean up remaining files in the directory
for f in os.listdir(local_dir):
    os.remove(os.path.join(local_dir, f))

# If data is available, proceed with processing
if not df_merge.empty:
    # Function to convert bytes to kWh
    def bytes_to_kwh():
        """Convert bytes to kilowatt-hours (kWh)."""
        return (1 / 1_000_000_000) * 0.813420622  # Conversion factor

    # Function to get the current UK carbon intensity
    def get_uk_carbon_intensity():
        """Fetch the current carbon intensity of the UK grid."""
        headers = {'Accept': 'application/json'}
        response = requests.get('https://api.carbonintensity.org.uk/intensity', headers=headers)
        return response.json()['data'][0]['intensity']['actual'] if response.status_code == 200 else 448  # Default value

    # Function to get the carbon intensity of data centers based on IP location
    def get_data_center_carbon_intensity(ip):
        """Get the carbon intensity of a data center based on its IP location."""
        try:
            df_countries = pd.read_csv("/Users/colineritz/Desktop/Master_project/Data_pcap/energy_c02.csv"))
            response = requests.get(f'http://ip-api.com/json/{ip}', headers={'Accept': 'application/json'})
            if response.status_code == 200 and response.json()['status'] == 'success':
                country = response.json()['country']
                carbon_intensity = df_countries[df_countries['country_or_region'] == country]['emissions_intensity_gco2_per_kwh'].values[0]
            else:
                carbon_intensity = df_countries[df_countries['country_or_region'] == 'World']['emissions_intensity_gco2_per_kwh'].values[0]
        except:
            carbon_intensity = 448  # Default value
        return carbon_intensity

    # Function to calculate total CO2 emissions
    def calculate_total_co2():
        """Calculate total CO2 emissions based on energy consumption and carbon intensity."""
        world_carbon_intensity = 442.37
        return (0.52 * get_uk_carbon_intensity() + 
                0.14 * world_carbon_intensity + 
                0.19 * world_carbon_intensity + 
                0.15 * get_data_center_carbon_intensity(ip))

    # Function to convert kWh to grams of CO2
    def kwh_to_gco2():
        """Convert kWh to grams of CO2."""
        return bytes_to_kwh() * calculate_total_co2()

    # Load application labels
    label_path = '/Users/colineritz/Desktop/csv/Label.csv'
    df_label = pd.read_csv(label_path, on_bad_lines='skip')

    # Process and clean the merged data
    df_merge = df_merge[['c_to_s_bytes', 'ndpi_proto', 's_to_c_bytes', 'duration']]
    df_merge.replace("", np.nan, inplace=True)
    df_merge.dropna(inplace=True)

    # Map application names to labels
    df_merge['ndpi_proto'] = df_merge['ndpi_proto'].map(dict(zip(df_label['ndpi_proto'], df_label['Label'])))

    # Calculate CO2 emissions
    df_merge['Bytes'] = df_merge['c_to_s_bytes'] + df_merge['s_to_c_bytes']
    df_merge['carbon_footprint'] = df_merge['Bytes'] * kwh_to_gco2()
    df_merge.rename(columns={'ndpi_proto': 'Application'}, inplace=True)

    # Aggregate data by application
    df_new = df_merge.groupby('Application')['carbon_footprint'].sum().reset_index()

    # Save the results to a CSV file
    output_path = '/Users/colineritz/Desktop/output/co2_data/output.csv'
    df_new.to_csv(output_path, index=False)

    # Upload the results to Google Cloud Storage
    def upload_to_bucket(bucket_name, blob_name, file_path):
        """Upload a file to a Google Cloud Storage bucket."""
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return blob

    upload_to_bucket('three_user', 'output.csv', output_path)

# Stop the EmissionsTracker and print the total execution time
t1 = time.time()
total_time = t1 - t0
tracker.stop()
print(f"Total execution time: {total_time} seconds")