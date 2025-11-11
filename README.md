# PCMonitor
---
## Grafana Dashboard
<img width="1280" height="695" alt="Image" src="https://github.com/user-attachments/assets/627e4da9-7b8d-4991-ad15-b4c8c2edefc8" />

Before I took this screenshot, I launched Battlefield 6 -- you can see the resource spike.

## Architecture Diagram
<img width="761" height="441" alt="Image" src="https://github.com/user-attachments/assets/43adc34f-8951-4af7-ba06-a3f32a232332" />

### Explanation
This repo contains the monitor.py and requirements.txt files.

- monitor.py is used to create a Windows Service name PCMonitor, with auto start and restart capabilities.
    - INTERVAL inside monitor.py dictates how often it sends data to the InfluxDB bucket.

- monitor.py uses the InfluxDB_client module to initialize an InfluxDB Client as part of the Windows Service, and then the rest of the script uses the write_api to send the CPU/GPU data to the InfluxDB container.
    - This is sent as an HTTP POST request to the InfluxDB container running on my Unraid home lab, with the data in Line Protocol Format. Benefits of the Line Protocol: 
        - More compact, efficient, and faster to parse since it just simple text. 
        - Mainly, this format has less bandwidth than JSON/XML which is great because I want this service to be as light as possible since it is also my gaming computer.

- nssm.exe was then used to turn the monitor.py file into a Windows Service, with auto start and restart capabilities
> ![IMPORTANT NOTE]
    Because of how difficult it is to read CPU temperatures via Python on Windows machine, PyLibreHardwareMonitor is the library used. PyLibreHardwareMonitor *requires Administrative privileges to run*,  which nssm.exe made easy to set up.

### While Running
The PCMonitor service runs, sending data every 10 seconds (default) via HTTP POST request to the InfluxDB container.

Grafana then consumes the time-series data by using InfluxDB as a data source. Then I made a Grafana dashboard with Flux queries.

