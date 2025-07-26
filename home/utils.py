# import subprocess
# import re
# import platform
# import paramiko

# def discover_devices():
#     """Finds devices on the local network using arp (Windows) or ip neigh (Linux)."""
#     try:
#         os_type = platform.system()
#         if os_type == "Windows":
#             output = subprocess.check_output("arp -a", shell=True).decode()
#         else:  # Linux
#             output = subprocess.check_output("ip neigh", shell=True).decode()

#         devices = re.findall(r"(\d+\.\d+\.\d+\.\d+)", output)
#         return devices
#     except Exception as e:
#         return {"error": str(e)}

# def get_client_info(ip, username, password):
#     """Fetch system info via SSH."""
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(ip, username=username, password=password, timeout=5)

#         stdin, stdout, stderr = ssh.exec_command("uname -a")
#         system_info = stdout.read().decode()

#         ssh.close()
#         return {"system_info": system_info}
#     except Exception as e:
#         return {"error": str(e)}


import socket
import ipaddress
from .models import ConnectedPC  # Replace with your actual app

def scan_network():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        network = ipaddress.ip_network(f"{local_ip}/24", strict=False)

        for ip in network:
            ip_str = str(ip)
            try:
                hostname, _, _ = socket.gethostbyaddr(ip_str)
                obj, created = ConnectedPC.objects.update_or_create(
                    ip_address=ip_str,
                    defaults={"name": hostname}
                )
                if created:
                    print(f"New device added: {hostname} ({ip_str})")
                else:
                    print(f"Device updated: {hostname} ({ip_str})")
            except (socket.herror, socket.gaierror):
                continue  
    except Exception as e:
        print("Error scanning network:", e)
