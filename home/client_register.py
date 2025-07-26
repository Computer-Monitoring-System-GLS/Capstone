import requests
import socket
import json

# Import existing system info functions
from home import get_os_info, get_cpu_info, get_ram_info

# Function to gather system information
def collect_system_data():
    return {
        "hostname": socket.gethostname(),
        "os": get_os_info(),
        "cpu": get_cpu_info(),
        "ram": get_ram_info()
    }

# Function to send system info to Django server
def send_data_to_server():
    server_url = "http://192.168.0.109:8000/system_info"  # Use Django server IP & port
    data = collect_system_data()
    
    try:
        response = requests.post(server_url, json=data)
        print(response.json())  # Print server response
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

# Run the function
if __name__ == "__main__":
    send_data_to_server()
