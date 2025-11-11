import PyLibreHardwareMonitor as plhm
import time, socket
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from InfluxDB_config import url, token, org, bucket

url = url
token = token
org = org
bucket = bucket
hostname = socket.gethostname()
INTERVAL = 10  #this is in seconds

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def get_cpu(hostname):
    """
        Captures CPU data.
        GETTING THE CPU TEMP ON WINDOWS WITH PYTHON IS AN UNUSUALLY CRUEL AND TORTUROUS PUNISHMENT.
    """
    cpu_data = {}

    monitor = plhm.Computer()
    cpu = monitor.cpu

    cpu_data['Temperature'] = round(cpu["AMD Ryzen 7 5800X3D"]["Temperature"]["Core (Tctl/Tdie)"], 2)
    cpu_data['Load'] = round(cpu["AMD Ryzen 7 5800X3D"]["Load"]["CPU Total"], 2)
    cpu_data['Core 1 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #1"]
    cpu_data['Core 2 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #2"]
    cpu_data['Core 3 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #3"]
    cpu_data['Core 4 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #4"]
    cpu_data['Core 5 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #5"]
    cpu_data['Core 6 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #6"]
    cpu_data['Core 7 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #7"]
    cpu_data['Core 8 Frequency'] = cpu["AMD Ryzen 7 5800X3D"]["Clock"]["Core #8"]
    cpu_data['Power'] = cpu["AMD Ryzen 7 5800X3D"]["Power"]["Package"] # idk what this unit is yet

    point = Point("cpu_stats") \
        .tag("host", hostname) \
        .field("Temperature", cpu_data['Temperature']) \
        .field("Load", cpu_data['Load']) \
        .field("Core 1 Frequency", cpu_data['Core 1 Frequency']) \
        .field("Core 2 Frequency", cpu_data['Core 2 Frequency']) \
        .field("Core 3 Frequency", cpu_data['Core 3 Frequency']) \
        .field("Core 4 Frequency", cpu_data['Core 4 Frequency']) \
        .field("Core 5 Frequency", cpu_data['Core 5 Frequency']) \
        .field("Core 6 Frequency", cpu_data['Core 6 Frequency']) \
        .field("Core 7 Frequency", cpu_data['Core 7 Frequency']) \
        .field("Core 8 Frequency", cpu_data['Core 8 Frequency']) \
        .field("Power", cpu_data['Power']) \
    
    return point
    

def get_gpu(hostname):
    """
        Captures GPU data.
    """
    gpu_data = {}
    
    monitor = plhm.Computer()
    gpu = monitor.gpu

    gpu_data['Temperature'] = gpu["NVIDIA GeForce RTX 5080"]["Temperature"]["GPU Core"]
    gpu_data['Frequency'] = gpu["NVIDIA GeForce RTX 5080"]["Clock"]['GPU Core']
    gpu_data['Memory Used'] = gpu["NVIDIA GeForce RTX 5080"]["SmallData"]["GPU Memory Used"]
    gpu_data['Memory Free'] = gpu["NVIDIA GeForce RTX 5080"]["SmallData"]["GPU Memory Free"]
    gpu_data['Power'] = gpu["NVIDIA GeForce RTX 5080"]["Power"]["GPU Package"]

    point = Point("gpu_stats") \
        .tag("host", hostname) \
        .field('Temperature', gpu_data['Temperature']) \
        .field('Frequency', gpu_data['Frequency']) \
        .field('Memory Used', gpu_data['Memory Used']) \
        .field('Memory Free', gpu_data['Memory Free']) \
        .field('Power', gpu_data['Power']) \

    return point

def collect_metrics(write_api, bucket, hostname):
    while True:
        cpu_point = get_cpu(hostname)
        write_api.write(bucket=bucket, record=cpu_point)

        gpu_point = get_gpu(hostname)
        write_api.write(bucket=bucket, record=gpu_point)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    collect_metrics(write_api=write_api, bucket=bucket, hostname=hostname)