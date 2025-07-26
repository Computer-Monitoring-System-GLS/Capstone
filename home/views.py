# from django.http import HttpResponseRedirect, JsonResponse
# from django.shortcuts import render, redirect
# from django.core.cache import cache
# from django.contrib import messages
# import platform
# import subprocess
# import re
# from .forms import LoginForm
# import nmap
# import socket
# import paramiko
# import psutil
# from django.shortcuts import render
# import socket
# import sys
# import os
# import json
# import datetime

# def get_local_ip():
#     """Get the current device's local IP address."""
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(("8.8.8.8", 80))
#         local_ip = s.getsockname()[0]
#         s.close()
#         return local_ip
#     except socket.error as e:
#         print(f"Error getting local IP: {e}")
#         return "Unknown"

# def check_ssh(ip):
#     """Check if SSH is available on a device."""
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(1)  # Timeout in seconds
#     result = sock.connect_ex((ip, 22))
#     sock.close()
#     return result == 0  # True if SSH is open, False otherwise

# def get_network_devices():
#     """Scan network for all connected devices and check SSH availability."""
#     nm = nmap.PortScanner()
#     local_ip = get_local_ip()
#     network_range = ".".join(local_ip.split(".")[:3]) + ".0/24"  # Example: 192.168.1.0/24

#     try:
#         print(f"Scanning network: {network_range}")  # Debugging log
#         nm.scan(hosts=network_range, arguments="-sn")  # Ping scan (detects all devices)
#         devices = []

#         for host in nm.all_hosts():
#             has_ssh = check_ssh(host)  # Check if SSH is available
#             devices.append({
#                 "ip": host,
#                 "is_self": (host == local_ip),
#                 "has_ssh": has_ssh
#             })

#         print("Detected Devices:", devices)  # Debugging log
#         return devices

#     except Exception as e:
#         print(f"Error scanning network: {e}")
#         return []

# def get_system_info():
#     """Retrieve local system details."""
#     return {
#         "ip": get_local_ip(),
#         "cpu": f"{psutil.cpu_percent()}% CPU usage",
#         "ram": f"{psutil.virtual_memory().percent}% RAM usage",
#         "disk": f"{psutil.disk_usage('/').percent}% Disk usage"
#     }


# def get_network_devices():
#     """Scan network for all connected devices and check SSH availability."""
#     nm = nmap.PortScanner()
#     local_ip = get_local_ip()
#     network_range = "{}.{}.{}.0/24".format(*local_ip.split(".")[:3])

#     try:
#         print(f"Scanning network: {network_range}")
#         nm.scan(hosts=network_range, arguments="-sn")
#         devices = []

#         for host in nm.all_hosts():
#             has_ssh = check_ssh(host)
#             devices.append({"ip": host, "is_self": (host == local_ip), "has_ssh": has_ssh})

#         print("Detected Devices:", devices)
#         return devices
#     except Exception as e:
#         print(f"Error scanning network: {e}")
#         return []


# def get_remote_info(ip, username, password):
#     """Fetch system details from a remote Windows device via SSH."""
#     try:
#         print(f"🔌 Connecting to {ip} via SSH as {username}...")  

#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         client.connect(ip, username=username, password=password, timeout=10)

#         commands = {
#             "OS Info": "wmic os get Caption",
#             "CPU Info": "wmic cpu get Name",
#             "Motherboard Info": "wmic baseboard get Product",
#             "GPU Info": "wmic path win32_videocontroller get Caption",
#             "RAM Info": "wmic memorychip get Capacity",
#             "Storage Info": "wmic logicaldisk get Size",
#             "Audio Info": "wmic sounddev get Caption",
#             "Network Info": "wmic nic where NetEnabled=true get Name",
#             "Peripherals Info": "wmic path Win32_PnPEntity get Name",
#             "Software Installed": "wmic product get Name"
#         }

#         device_info = {"ip": ip}

#         for key, cmd in commands.items():
#             stdin, stdout, stderr = client.exec_command(cmd)
#             # output = stdout.read().decode().strip()
#             # error = stderr.read().decode().strip()
#             output = stdout.read().decode("latin-1").strip()
#             error = stderr.read().decode("latin-1").strip()
#             # output = stdout.read().decode("utf-8", errors="ignore").strip()
#             # error = stderr.read().decode("utf-8", errors="ignore").strip()

            
#             if error:
#                 print(f"⚠ Command '{cmd}' failed: {error}")
#                 device_info[key] = f"Error: {error}"
#             else:
#                 print(f"✅ {key}: {output}")
#                 device_info[key] = output if output else "N/A"

#         client.close()
#         print(f"✅ Successfully fetched details for {ip}: {device_info}")

#         return device_info

#     except paramiko.AuthenticationException:
#         print(f"❌ Authentication failed for {ip}!")
#         return {"error": "Authentication failed. Please check your username and password."}

#     except paramiko.SSHException as e:
#         print(f"❌ SSH error for {ip}: {e}")
#         return {"error": f"SSH error: {e}"}

#     except Exception as e:
#         print(f"❌ Connection failed for {ip}: {e}")
#         return {"error": f"Failed to fetch remote info: {e}"}



# def device_list(request):
#     """Render a list of detected devices."""
#     devices = get_network_devices()
#     return render(request, "device_list.html", {"devices": devices})

# # def device_summary(request, ip):
# #     """Fetch system info for the selected device."""
    
# #     username = request.GET.get("username", "").strip()
# #     password = request.GET.get("password", "").strip()

# #     print(f"🔍 Received Request for IP: {ip}")
# #     print(f"👤 Username: {username}, Password: {'*' * len(password)}")  # Masked password

# #     if not username or not password:
# #         return render(request, "summary.html", {"error": "SSH credentials are required!"})

# #     print(f"🔌 Fetching REMOTE system info for {ip} via SSH as {username}")

# #     data = get_remote_info(ip, username=username, password=password)

# #     if "error" in data:
# #         print(f"❌ SSH Fetch Failed: {data['error']}")
# #         return render(request, "summary.html", {"error": data["error"]})

# #     json_path = save_device_data(ip, data)
# #     print(f"✅ System info stored in: {json_path}")

# #     return render(request, "summary.html", {"device_info": data})


# def device_summary(request, ip):
#     """Fetch and store all system info categories for a device while keeping the HTML view intact."""
#     local_ip = get_local_ip()
#     print(f"🔍 Fetching all system info for device: {ip}")

#     username = request.GET.get("username", "").strip()
#     password = request.GET.get("password", "").strip()

#     print(f"👤 Username: {username}, Password: {'*' * len(password)}")  # Masked password

#     if not username or not password:
#         print("❌ Missing SSH credentials!")
#         return render(request, "summary.html", {"error": "SSH credentials are required!"})

#     if ip == local_ip:
#         print("📌 Fetching LOCAL system info...")
#         data = {
#             "OS": get_os_info(),
#             "CPU": get_cpu_info(),
#             "Motherboard": get_motherboard_info(),
#             "GPU": get_gpu_info(),
#             "RAM": get_ram_info(),
#             "Storage": get_storage_info(),
#             "Audio": get_audio_info(),
#             "Network": get_network_info(),
#             "Peripherals": get_peripherals_info(),
#             "Software": get_software()
#         }
#     else:
#         print(f"🔌 Attempting SSH connection to {ip} as {username}...")
#         device_info = get_remote_info(ip, username=username, password=password)

#         if not device_info or "error" in device_info:
#             print(f"❌ SSH Fetch Failed: {device_info.get('error', 'Unknown error')}")
#             return render(request, "summary.html", {"error": device_info.get("error", "SSH Connection Failed!")})

#         data = {
#             "OS": device_info.get("OS Info", {}),
#             "CPU": device_info.get("CPU Info", {}),
#             "Motherboard": device_info.get("Motherboard Info", {}),
#             "GPU": device_info.get("GPU Info", {}),
#             "RAM": device_info.get("RAM Info", {}),
#             "Storage": device_info.get("Storage Info", {}),
#             "Audio": device_info.get("Audio Info", {}),
#             "Network": device_info.get("Network Info", {}),
#             "Peripherals": device_info.get("Peripherals Info", {}),
#             "Software": device_info.get("Software Installed", {})
#         }

#     json_path = save_device_data(ip, data)
#     print(f"✅ System info stored in: {json_path}")

#     return render(request, "summary.html", {"device_info": data})



# # def save_device_data(ip, data):
# #     """Helper function to save system info to a JSON file."""
    
# #     os.makedirs("device_data", exist_ok=True)  # Ensure directory exists
# #     json_filename = f"{ip}.json"
# #     json_path = os.path.join("device_data", json_filename)

# #     # Add timestamp
# #     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #     data_with_timestamp = {"Last Updated": timestamp, **data}

# #     with open(json_path, "w") as json_file:
# #         json.dump(data_with_timestamp, json_file, indent=4)

# #     print(f"✅ Data saved at: {json_path} (Updated on: {timestamp})")
# #     return json_path

# def save_device_data(ip, data):
#     """Helper function to save system info to a JSON file."""

#     os.makedirs("device_data", exist_ok=True)  # Ensure directory exists
#     json_filename = f"{ip}.json"
#     json_path = os.path.join("device_data", json_filename)

#     # Add timestamp
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     data_with_timestamp = {"Last Updated": timestamp, **data}

#     try:
#         # Write JSON data to file
#         with open(json_path, "w", encoding="utf-8") as json_file:
#             json.dump(data_with_timestamp, json_file, indent=4)
        
#         # Verify if the file is written correctly
#         with open(json_path, "r", encoding="utf-8") as json_file:
#             saved_data = json.load(json_file)

#         if not saved_data:
#             print("⚠ JSON file saved but is empty! Something went wrong.")
#         else:
#             print(f"✅ Data successfully saved at: {json_path} (Updated on: {timestamp})")

#     except Exception as e:
#         print(f"❌ Error saving JSON file: {e}")

#     return json_path



# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             serial_no = form.cleaned_data.get('serial_no')
#             password = form.cleaned_data.get('password')
#             # TODO: Implement authentication logic here
#             messages.error(request, 'Invalid credentials')
#             return redirect('device_list')
#             # return redirect('index')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


# def run_command(command):
#     try:
#         # result = subprocess.check_output(command, shell=True, text=True).strip()
#         result = subprocess.check_output(command, shell=True, text=True)
#         return result
#         # return result.strip()
#     except subprocess.CalledProcessError as e:
#         return f"Error: {e}"

# def get_wifi_ipv4():
#     try:
#         # Running ipconfig to get all adapter details
#         ipconfig_output = run_command("ipconfig")

#         # Searching for the "Wireless LAN adapter Wi-Fi" section and the corresponding IPv4 Address
#         wifi_ipv4 = None
#         wifi_section_found = False

#         # Splitting the output into lines to process each line
#         for line in ipconfig_output.splitlines():
#             # Check if the current line is in the Wireless LAN adapter Wi-Fi section
#             if "Wireless LAN adapter Wi-Fi" in line:
#                 wifi_section_found = True
#             elif wifi_section_found and "IPv4 Address" in line:  # Once we find the Wi-Fi section, look for IPv4
#                 match = re.search(r"IPv4 Address(?:[^\r\n]*):\s+([\d.]+)", line)
#                 if match:
#                     wifi_ipv4 = match.group(1)
#                 break  # Stop once we find the IPv4 address
        
#         return wifi_ipv4 if wifi_ipv4 else "Not Available"

#     except Exception as e:
#         return f"Error: {str(e)}"

# def get_summary():
#     try:
#         os_type = platform.system()
#         if os_type == "Windows":
#             os_name = run_command("wmic os get Caption | findstr /V Caption")
#             cpu_name = run_command("wmic cpu get name | findstr /V Name")
#             ram_size = run_command("wmic memorychip get Capacity | findstr /V Capacity")
#             motherboard1 = run_command("wmic baseboard get Manufacturer | findstr /V Manufacturer")
#             motherboard2 = run_command("wmic baseboard get Product | findstr /V Product")
#             graphics = run_command("wmic path Win32_VideoController get Name | findstr /V Name")
#             storage = run_command("wmic diskdrive get Size | findstr /V Size")
#             network = get_wifi_ipv4()
#             audio = run_command("wmic sounddev get Name | findstr /V Name")

#             # Convert RAM size from bytes to GB
#             if ram_size:
#                 size_gb = [f"{int(int(s.strip()) / 1073741824)}GB" for s in ram_size.splitlines() if s.strip().isdigit()]
#                 ram_size = " + ".join(size_gb) if size_gb else "Not Available"
#             else:
#                 ram_size = "Not Available"

#             # Convert storage from bytes to GB (1 GB = 1073741824 bytes)
#             if storage:
#                 storage_gb = [f"{int(int(size.strip()) / 1073741824)}GB" for size in storage.splitlines() if size.strip().isdigit()]
#                 storage = ", ".join(storage_gb) if storage_gb else "Not Available"
#             else:
#                 storage = "Not Available"

#         else:  # Linux Commands
#             os_name = run_command("lsb_release -d | awk -F'\t' '{print $2}'")
            
#         return {
#             "Summary": {
#                 "Operating System": os_name.strip() if os_name else "Not Available",
#                 "CPU": cpu_name.strip() if cpu_name else "Not Available",
#                 "RAM": ram_size,
#                 "Motherboard": f"{motherboard1.strip()} {motherboard2.strip()}".strip() if motherboard1 or motherboard2 else "Not Available",
#                 "Graphics": graphics.strip() if graphics else "Not Available",
#                 "Storage": storage,
#                 "Network": network.strip() if network else "Not Available",
#                 "Audio": audio.strip() if audio else "Not Available",
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}


# def get_os_info():
#     try:
#         os_type = platform.system()

#         if os_type == "Windows":
#             os_name = run_command("wmic os get Caption | findstr /V Caption")
#             os_version = run_command("wmic os get Version | findstr /V Version")
#             os_architecture = run_command("wmic os get OSArchitecture | findstr /V OSArchitecture")
#             wifi_ipv4_address = get_wifi_ipv4()
#             os_manufacturer = run_command("wmic os get Manufacturer | findstr /V Manufacturer")
#             os_serialno = run_command("wmic os get SerialNumber | findstr /V SerialNumber")
#             os_installdate = run_command("wmic os get InstallDate | findstr /V InstallDate")
#             # os_uac_name = run_command("wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName | findstr /V displayName")
#             # os_uac_path = run_command("wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get pathToSignedProductExe | findstr /V pathToSignedProductExe")
#             firewall_name = run_command("wmic service where Name='mpssvc' get Name | findstr /V Name")
#             firewall_startmode = run_command("wmic service where Name='mpssvc' get StartMode | findstr /V StartMode")
#             firewall_status = run_command("wmic service where Name='mpssvc' get State | findstr /V Status")
#             autoupdt_caption = run_command("wmic qfe get Caption | findstr /V Caption")
#             autoupdt_instlledon = run_command("wmic qfe get InstalledOn | findstr /V InstalledOn")
#             autoupdt_hotfixid = run_command("wmic qfe get HotFixID | findstr /V HotFixID")
#             battery_status = run_command("wmic path Win32_Battery get BatteryStatus | findstr /V BatteryStatus")
#             battery_remain = run_command(" wmic path Win32_Battery get EstimatedChargeRemaining | findstr /V EstimatedChargeRemaining")
        
#         else:    #Linux
#             os_name = run_command("lsb_release -d | awk -F'\t' '{print $2}'")

#         return {
#             "OS Info": {
#                 "OS Name": os_name.strip() if os_name else "Not Available",
#                 "OS Version": os_version.strip() if os_version else "Not Available",
#                 "OS Architecture": os_architecture.strip() if os_architecture else "Not Available",
#                 "Wi-Fi IPv4 Address": wifi_ipv4_address,
#                 "Manufacturer": os_manufacturer.strip() if os_manufacturer else "Not Available",
#                 "Serial Number": os_serialno.strip() if os_serialno else "Not Available",
#                 "Install Date": os_installdate.strip() if os_installdate else "Not Available",
#                 # "UAC Name": os_uac_name.strip() if os_uac_name else "Not Available",
#                 # "UAC Path": os_uac_path.strip() if os_uac_path else "Not Available",
#                 "Firewall Name": firewall_name.strip() if firewall_name else "Not Available",
#                 "Firewall StartMode": firewall_startmode.strip() if firewall_startmode else "Not Available",
#                 "Firewall Status": firewall_status.strip() if firewall_status else "Not Available",
#                 "AutoUpdate Caption": autoupdt_caption.strip() if autoupdt_caption else "Not Available",
#                 "AutoUpdate InstalledOn": autoupdt_instlledon.strip() if autoupdt_instlledon else "Not Available",
#                 "AutoUpdate HotFixID": autoupdt_hotfixid.strip() if autoupdt_hotfixid else "Not Available",
#                 "Battery Status": battery_status.strip() if battery_status else "Not Available",
#                 "Charging Remaining": battery_remain.strip() if battery_remain else "Not Available",
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}
    
# def get_cpu_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             cpu_name = run_command("wmic cpu get name | findstr /V Name")
#             cpu_architecture = run_command("wmic cpu get architecture | findstr /V Architecture")
#             cpu_socketdesignation = run_command("wmic cpu get SocketDesignation | findstr /V SocketDesignation")
#             cpu_nocores = run_command("wmic cpu get NumberOfCores | findstr /V NumberOfCores")
#             cpu_logicalproc = run_command("wmic cpu get NumberOfLogicalProcessors | findstr /V NumberOfLogicalProcessors")
#             cpu_frequency = run_command("wmic cpu get CurrentClockSpeed | findstr /V CurrentClockSpeed")
#             cpu_loadper = run_command("wmic cpu get LoadPercentage | findstr /V LoadPercentage")
#             cpu_family = run_command("wmic cpu get Family | findstr /V Family")
#             cpu_descp = run_command("wmic cpu get Description | findstr /V  Description")
#             cpu_processorid = run_command("wmic cpu get ProcessorId | findstr /V ProcessorId")
#             cpu_manufacturer = run_command("wmic cpu get Manufacturer | findstr /V Manufacturer")
#             cpu_deviceid = run_command("wmic cpu get DeviceID | findstr /V DeviceID")
#             cpu_stock = run_command("wmic cpu get MaxClockSpeed | findstr /V MaxClockSpeed")
#             cpu_buspeed = run_command("wmic cpu get ExtClock | findstr /V ExtClock")
#             cpu_vir = run_command("wmic cpu get VirtualizationFirmwareEnabled | findstr /V VirtualizationFirmwareEnabled")
#             cpu_l2 = run_command("wmic cpu get L2CacheSize | findstr /V L2CacheSize")
#             cpu_l3 = run_command("wmic cpu get L3CacheSize | findstr /V L3CacheSize")
#             # cpu_temp = run_command('powershell -Command "((Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace \\"root/wmi\\").CurrentTemperature - 2732) / 10"')

#         else: #Linux
#             cpu_name = run_command("lscpu | grep 'Model name' | awk -F: '{print $2}'")
#             cpu_nocores = run_command("lscpu | grep '^Core(s) per socket' | awk '{print $NF}'")
#             cpu_logicalproc = run_command("nproc")
#             cpu_frequency = run_command("lscpu | grep 'MHz' | awk '{print $NF}'")
#             cpu_manufacturer = run_command("cat /proc/cpuinfo | grep 'vendor_id' | uniq | awk '{print $3}'")

#         return {
#             "CPU Info": {
#                 "CPU Name": cpu_name.strip() if cpu_name else "Not Available",
#                 "CPU Architecture": cpu_architecture.strip() if cpu_architecture else "Not Available",
#                 "Socket Designation": cpu_socketdesignation.strip() if cpu_socketdesignation else "Not Available",
#                 "Number Of Cores" : cpu_nocores.strip() if cpu_nocores else "Not Available",
#                 "Number Of Logical Processors": cpu_logicalproc.strip() if cpu_logicalproc else "Not Available",
#                 "Frequency" : cpu_frequency.strip() if cpu_frequency else "Not Available",
#                 "Load Percentage" : cpu_loadper.strip() if cpu_loadper else "Not Available",
#                 "Description": cpu_descp.strip() if cpu_descp else "Not Available",
#                 "Family": cpu_family.strip() if cpu_family else "Not Available",
#                 "Processor ID": cpu_processorid.strip() if cpu_processorid else "Not Available",
#                 "Manufacturer": cpu_manufacturer.strip() if cpu_manufacturer else "Not Available",
#                 "Device ID": cpu_deviceid.strip() if cpu_deviceid else "Not Available",
#                 "Stock Core Speed": cpu_stock.strip() if cpu_stock else "Not Available",
#                 "Bus Speed": cpu_buspeed.strip() if cpu_buspeed else "Not Available",
#                 "Virtualization": cpu_vir.strip() if cpu_vir else "Not Available",
#                 "L2 Cache Size": cpu_l2.strip() if cpu_l2 else "Not Available",
#                 "L3 Cache Size": cpu_l3.strip() if cpu_l3 else "Not Available",
#                 # "CPU Temperature" : cpu_temp.strip(),
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}


# def get_motherboard_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             motherboard_manufacturer = run_command("wmic baseboard get Manufacturer | findstr /V Manufacturer")
#             motherboard_product = run_command("wmic baseboard get Product | findstr /V Product")
#             motherboard_version = run_command("wmic baseboard get Version | findstr /V Version")
#             motherboard_serial = run_command("wmic baseboard get SerialNumber | findstr /V SerialNumber")
#             bios_manufacturer = run_command("wmic bios get Manufacturer | findstr /V Manufacturer")
#             bios_version = run_command("wmic bios get Version | findstr /V Version")
#             bios_release_date = run_command("wmic bios get ReleaseDate | findstr /V ReleaseDate")
#             memorychip_manufacturer = run_command("wmic memorychip get Manufacturer | findstr /V Manufacturer")
#             memorychip_capacity = run_command("wmic memorychip get Capacity | findstr /V Capacity")
#             memorychip_deviceloc = run_command("wmic memorychip get DeviceLocator | findstr /V DeviceLocator")
#             memorychip_partno = run_command("wmic memorychip get PartNumber | findstr /V PartNumber")
#             memorychip_speed = run_command("wmic memorychip get Speed | findstr /V Speed")
#             memorychip_type = run_command("wmic memorychip get MemoryType | findstr /V MemoryType")
#             usb_name = run_command("wmic path Win32_USBController get Name | findstr /V Name")
#             usb_description = run_command("wmic path Win32_USBHub get Description | findstr /V Description")
#             usb_status = run_command("wmic path Win32_USBController get Status | findstr /V Status")
#             pcie_name = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get Name | findstr /V Name")
#             pcie_deviceid = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get DeviceID | findstr /V DeviceID")
#             pcie_manuf = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get Manufacturer | findstr /V Manufacturer")
#             netadpt_name = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get Name | findstr /V Name")
#             netadpt_netconnid = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get NetConnectionID | findstr /V NetConnectionID")
#             netadpt_adptype = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get AdapterType | findstr /V AdapterType")
#             netadpt_macadd = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get MACAddress | findstr /V MACAddress")
        
#         else:  #Linux
#             motherboard_manufacturer = run_command("sudo dmidecode -t baseboard")

#         return {
#             "Motherboard Info": {
#                 "Manufacturer": motherboard_manufacturer.strip() if motherboard_manufacturer else "Not Available",
#                 "Product": motherboard_product.strip() if motherboard_product else "Not Available",
#                 "Version": motherboard_version.strip() if motherboard_version else "Not Available",
#                 "Serial Number": motherboard_serial.strip() if motherboard_serial else "Not Available",
#                 "Bios Manufacturer": bios_manufacturer.strip() if bios_manufacturer else "Not Available",
#                 "Bios Version": bios_version.strip() if bios_version else "Not Available",
#                 "Bios Release Date": bios_release_date.strip() if bios_release_date else "Not Available",
#                 "Memory Chip Manufacturer" : memorychip_manufacturer.strip() if memorychip_manufacturer else "Not Available",
#                 "Memory Chip Capacity" : memorychip_capacity.strip() if memorychip_capacity else "Not Available",
#                 "Memory Chip Device Locator" : memorychip_deviceloc.strip() if memorychip_deviceloc else "Not Available",
#                 "Memory Chip Part Number" : memorychip_partno.strip() if memorychip_partno else "Not Available",
#                 "Memory Chip Speed" : memorychip_speed.strip() if memorychip_speed else "Not Available",
#                 "Memory Chip Type" : memorychip_type.strip() if memorychip_type else "Not Available",
#                 "USB Name" : usb_name.strip() if usb_name else "Not Available",
#                 "USB Description" : usb_description.strip() if usb_description else "Not Available",
#                 "USB Status" : usb_status.strip() if usb_status else "Not Available",
#                 "PCIe Name" : pcie_name.strip() if pcie_name else "Not Available",
#                 "PCIe Device ID" : pcie_deviceid.strip() if pcie_deviceid else "Not Available",
#                 "PCIe Manufacturer" : pcie_manuf.strip() if pcie_manuf else "Not Available",
#                 "Network Adapter Name" : netadpt_name.strip() if netadpt_name else "Not Available",
#                 "Network Adapter Net Connection ID" : netadpt_netconnid.strip() if netadpt_netconnid else "Not Available",
#                 "Network Adapter Type" : netadpt_adptype.strip() if netadpt_adptype else "Not Available",
#                 "Network Adapter MACAddress" : netadpt_macadd.strip() if netadpt_macadd else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_gpu_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             monitor_caption = run_command("wmic desktopmonitor get Caption | findstr /V Caption")
#             monitor_deviceid = run_command("wmic desktopmonitor get DeviceID | findstr /V DeviceID")
#             monitor_pnpid = run_command("wmic desktopmonitor get PNPDeviceID | findstr /V PNPDeviceID")
#             gpu_name = run_command("wmic path Win32_VideoController get Name | findstr /V Name")
#             gpu_adptcomp = run_command("wmic path Win32_VideoController get AdapterCompatibility | findstr /V AdapterCompatibility")
#             gpu_pnpid = run_command("wmic path Win32_VideoController get PNPDeviceID | findstr /V PNPDeviceID")
#             gpu_vdprocessor = run_command("wmic path Win32_VideoController get VideoProcessor | findstr /V VideoProcessor")
#             gpu_driver = run_command("wmic path Win32_VideoController get DriverVersion | findstr /V DriverVersion")
#             gpu_curr_refreshrate = run_command("wmic path Win32_VideoController get CurrentRefreshRate | findstr /V CurrentRefreshRate")
#             gpu_currhor = run_command("wmic path Win32_VideoController get CurrentHorizontalResolution | findstr /V CurrentHorizontalResolution")
#             gpu_currvert = run_command("wmic path Win32_VideoController get CurrentVerticalResolution | findstr /V CurrentVerticalResolution")
#             gpu_currbits = run_command("wmic path Win32_VideoController get CurrentBitsPerPixel | findstr /V CurrentBitsPerPixel")
#             max_refresh = run_command("wmic path Win32_VideoController get MaxRefreshRate | findstr /V MaxRefreshRate")
#             min_refresh = run_command("wmic path Win32_VideoController get MinRefreshRate | findstr /V MinRefreshRate")
#             video_desp = run_command("wmic path Win32_VideoController get VideoModeDescription | findstr /V VideoModeDescription")
#             curr_nocolor = run_command("wmic path Win32_VideoController get CurrentNumberOfColors | findstr /V CurrentNumberOfColors")
        
#         else:  # For Linux or macOS
#             gpu_name = run_command('sudo lshw -C display')

#         return {
#             "GPU Info": {
#                 "Monitor Caption" : monitor_caption.strip() if monitor_caption else "Not Available",
#                 "Monitor DeviceID" : monitor_deviceid.strip() if monitor_deviceid else "Not Available",
#                 "Monitor PNPDeviceID" : monitor_pnpid.strip() if monitor_pnpid else "Not Available",
#                 "GPU Name" : gpu_name.strip() if gpu_name else "Not Available",
#                 "GPU AdapterCompatibility" : gpu_adptcomp.strip() if gpu_adptcomp else "Not Available",
#                 "GPU PNPDeviceID" : gpu_pnpid.strip() if gpu_pnpid else "Not Available",
#                 "GPU VideoProcessor" : gpu_vdprocessor.strip() if gpu_vdprocessor else "Not Available",
#                 "GPU Driver" : gpu_driver.strip() if gpu_driver else "Not Available",
#                 "GPU CurrentRefreshRate" : gpu_curr_refreshrate.strip() if gpu_curr_refreshrate else "Not Available",
#                 "GPU CurrentHorizontalResolution" : gpu_currhor.strip() if gpu_currhor else "Not Available",
#                 "GPU CurrentVerticalResolution" : gpu_currvert.strip() if gpu_currvert else "Not Available",
#                 "GPU CurrentBitsPerPixel" : gpu_currbits.strip() if gpu_currbits else "Not Available",
#                 "GPU MaxRefreshRate" : max_refresh.strip() if max_refresh else "Not Available",
#                 "GPU MinRefreshRate" : min_refresh.strip() if min_refresh else "Not Available",
#                 "GPU VideoModeDescription" : video_desp.strip() if video_desp else "Not Available",
#                 "GPU CurrentNumberOfColors" : curr_nocolor.strip() if curr_nocolor else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}


# def get_ram_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             physical_memory = run_command("wmic computersystem get TotalPhysicalMemory | findstr /V TotalPhysicalMemory")
#             memory_size = run_command("wmic OS get TotalVisibleMemorySize | findstr /V TotalVisibleMemorySize")
#             free_memory = run_command("wmic OS get FreePhysicalMemory | findstr /V FreePhysicalMemory")
#             total_virtual = run_command("wmic OS get TotalVirtualMemorySize | findstr /V TotalVirtualMemorySize")
#             free_virtual = run_command("wmic OS get FreeVirtualMemory | findstr /V FreeVirtualMemory")
#             capacity = run_command("wmic MemoryChip get Capacity | findstr /V Capacity")
#             memory_Type = run_command("wmic MemoryChip get MemoryType | findstr /V MemoryType")
#             speed = run_command("wmic MemoryChip get Speed | findstr /V  Speed")

#             if physical_memory:
#                 size_gb = [f"{int(int(s.strip()) / 1073741824)}GB" for s in physical_memory.splitlines() if s.strip().isdigit()]
#                 physical_memory = " + ".join(size_gb) if size_gb else "Not Available"
#             else:
#                 physical_memory = "Not Available"
        
#         else:  # For Linux or macOS
#             memory_size = run_command('sudo dmidecode --type memory | grep -i "Size"')

#         return {
#             "RAM Info": {
#                 "TotalPhysicalMemory" : physical_memory.strip() if physical_memory else "Not Available",
#                 "TotalVisibleMemorySize": memory_size.strip() if memory_size else "Not Available",
#                 "FreePhysicalMemory": free_memory.strip() if free_memory else "Not Available",
#                 "TotalVirtualMemorySize": total_virtual.strip() if total_virtual else "Not Available",
#                 "FreeVirtualMemory": free_virtual.strip() if free_virtual else "Not Available",
#                 "Capacity": capacity.strip() if capacity else "Not Available",
#                 "MemoryType": memory_Type.strip() if memory_Type else "Not Available",
#                 "Speed": speed.strip() if speed else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}
    
# def get_storage_info():
#     try:

#         os_type = platform.system()  # Make sure this is set properly

#         if os_type == "Windows":
#             diskdrive_deviceid = run_command("wmic diskdrive get DeviceID | findstr /V DeviceID")
#             diskdrive_model = run_command("wmic diskdrive get Model | findstr /V Model")
#             diskdrive_size = run_command("wmic diskdrive get Size | findstr /V Size")
#             diskdrive_interface = run_command("wmic diskdrive get InterfaceType | findstr /V InterfaceType")
#             diskdrive_status = run_command("wmic diskdrive get Status | findstr /V Status")
#             diskdrive_mediatype = run_command("wmic diskdrive get MediaType | findstr /V MediaType")
#             partition_name = run_command(" wmic partition get Name | findstr /V Name")
#             partition_index = run_command("wmic partition get Index | findstr /V Index")
#             partition_boot = run_command("wmic partition get BootPartition | findstr /V BootPartition")
#             partition_size = run_command("wmic partition get Size | findstr /V Size")
#             logicaldisk_deviceid = run_command("wmic logicaldisk get DeviceID | findstr /V DeviceID")
#             logicaldisk_filesys = run_command(" wmic logicaldisk get FileSystem | findstr /V FileSystem")
#             logicaldisk_size = run_command("wmic logicaldisk get Size | findstr /V Size")
#             logicaldisk_freespace = run_command("wmic logicaldisk get FreeSpace | findstr /V FreeSpace")
#             logicaldisk_volserialno = run_command("wmic logicaldisk get VolumeSerialNumber | findstr /V VolumeSerialNumber")
        
#         else:  # For Linux, using lsblk
#             diskdrive_mediatype = run_command("lsblk -d -o name,rota")

#         return {
#             "Storage Info": {
#                 "Disk Drive Device ID" : diskdrive_deviceid.strip() if diskdrive_deviceid else "Not Available",
#                 "Disk Drive Model" : diskdrive_model.strip() if diskdrive_model else "Not Available",
#                 "Disk Drive Size" : diskdrive_size.strip() if diskdrive_size else "Not Available",
#                 "Disk Drive Interface" : diskdrive_interface.strip() if diskdrive_interface else "Not Available",
#                 "Disk Drive Status" : diskdrive_status.strip() if diskdrive_status else "Not Available",
#                 "Disk Drive Media Type" : diskdrive_mediatype.strip() if diskdrive_mediatype else "Not Available",
#                 "Partition Name" : partition_name.strip() if partition_name else "Not Available",
#                 "Partition Index" : partition_index.strip() if partition_index else "Not Available",
#                 "Partition Boot" : partition_boot.strip() if partition_boot else "Not Available",
#                 "Partition Size" : partition_size.strip() if partition_size else "Not Available",
#                 "Logical Disk Device ID" : logicaldisk_deviceid.strip() if logicaldisk_deviceid else "Not Available",
#                 "Logical Disk File System" : logicaldisk_filesys.strip() if logicaldisk_filesys else "Not Available",
#                 "Logical Disk Size" : logicaldisk_size.strip() if logicaldisk_size else "Not Available",
#                 "Logical Disk Free Space" : logicaldisk_freespace.strip() if logicaldisk_freespace else "Not Available",
#                 "Logical Disk Volume Serial Number" : logicaldisk_volserialno.strip() if logicaldisk_volserialno else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_audio_info():
#     try:
#         os_type = platform.system()
        
#         if os_type == "Windows":
#             sound_card = run_command("wmic sounddev get Name | findstr /V Name")
#             playback = run_command('wmic path Win32_PnPEntity where "Name like \'%Audio%\'" get Name | findstr /V Name')
            
#             sound_card_list = sound_card.splitlines() if sound_card else []
#             playback_list = playback.splitlines() if playback else []
        
#         else:  # Linux Commands
#             playback = run_command("aplay -l")
#             playback_list = playback.splitlines() if playback else []
#             sound_card_list = []

#         # Clean up and remove empty lines
#         sound_card_list = [s.strip() for s in sound_card_list if s.strip()]
#         playback_list = [p.strip() for p in playback_list if p.strip()]

#         return {
#             "Audio Info": {
#                 "Sound Card": sound_card_list,  # Returning as a list
#                 "Playback": playback_list,  # Returning as a list
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_network_info():
#     try:
#         os_type = platform.system()
        
#         if os_type == "Windows":
#             internet_name = run_command(" wmic path Win32_NetworkAdapter where \"NetConnectionStatus=2\" get Name | findstr /V Name")
#             internet_connectstatus = run_command(" wmic path Win32_NetworkAdapter where \"NetConnectionStatus=2\" get NetConnectionStatus | findstr /V NetConnectionStatus")
#             networdadpt_name = run_command("wmic nic get Name | findstr /V Name")
#             networkadpt_netenable = run_command("wmic nic get NetEnabled | findstr /V NetEnabled")
#             networkadpt_macaddr = run_command("wmic nic get MACAddress | findstr /V MACAddress")
#             networkadpt_speed = run_command("wmic nic get Speed | findstr /V Speed")
#             networkadpt_adptype = run_command("wmic nic get AdapterType | findstr /V AdapterType")
#             descrp = run_command("wmic path Win32_NetworkAdapterConfiguration get Description | findstr /V Description")
#             ip_addr = run_command("wmic path Win32_NetworkAdapterConfiguration get IPAddress | findstr /V IPAddress")
#             mac_addr = run_command("wmic path Win32_NetworkAdapterConfiguration get MACAddress | findstr /V MACAddress")
#             ip_gateway = run_command("wmic path Win32_NetworkAdapterConfiguration get DefaultIPGateway | findstr /V DefaultIPGateway")
#             dns_server = run_command("wmic path Win32_NetworkAdapterConfiguration get DNSServerSearchOrder | findstr /V DNSServerSearchOrder")
#             dhcp_server = run_command("wmic path Win32_NetworkAdapterConfiguration get DHCPServer | findstr /V DHCPServer")
#             wifi_name = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get Name | findstr /V Name")
#             wifi_macaddr = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get MACAddress | findstr /V MACAddress")
#             wifi_speed = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get Speed | findstr /V Speed")
#             comp_name = run_command("wmic computersystem get Name | findstr /V Name")
#             comp_workgrp = run_command("wmic computersystem get Workgroup | findstr /V Workgroup")

#         else:  # Linux Commands
#             ip_addr = run_command("ip addr show")
            
#         return {
#             "Network Info": {
#                 "Internet Name" : internet_name.strip() if internet_name else "Not Available",
#                 "Internet ConnectStatus" : internet_connectstatus.strip() if internet_connectstatus else "Not Available",
#                 "Network Adapter Name" : networdadpt_name.strip() if networdadpt_name else "Not Available",
#                 "Network Adapter NetEnable" : networkadpt_netenable.strip() if networkadpt_netenable else "Not Available",
#                 "Network Adapter MACAddress" : networkadpt_macaddr.strip() if networkadpt_macaddr else "Not Available",
#                 "Network Adapter Speed" : networkadpt_speed.strip() if networkadpt_speed else "Not Available",
#                 "Network Adapter AdpType" : networkadpt_adptype.strip() if networkadpt_adptype else "Not Available",
#                 "Description" : descrp.strip() if descrp else "Not Available",
#                 "IP Address" : ip_addr.strip() if ip_addr else "Not Available",
#                 "MAC Address" : mac_addr.strip() if mac_addr else "Not Available",
#                 "IP Gateway" : ip_gateway.strip() if ip_gateway else "Not Available",
#                 "DNS Server" : dns_server.strip() if dns_server else "Not Available",
#                 "DHCP Server" : dhcp_server.strip() if dhcp_server else "Not Available",
#                 "Wi-Fi Name" : wifi_name.strip() if wifi_name else "Not Available",
#                 "Wi-Fi MACAddress" : wifi_macaddr.strip() if wifi_macaddr else "Not Available",
#                 "Wi-Fi Speed" : wifi_speed.strip() if wifi_speed else "Not Available",
#                 "Computer Name" : comp_name.strip() if comp_name else "Not Available",
#                 "Computer Workgroup" : comp_workgrp.strip() if comp_workgrp else "Not Available",
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_peripherals_info():
#     try:
#         os_type = platform.system()

#         if os_type == "Windows":
#             keyb_name = run_command("wmic path Win32_Keyboard get Name")
#             keyb_dscp = run_command("wmic path Win32_Keyboard get Description")
#             keyb_deviceid = run_command("wmic path Win32_Keyboard get DeviceID")
#             mouse_name = run_command("wmic path Win32_PointingDevice get Name")
#             mouse_deviceid = run_command("wmic path Win32_PointingDevice get DeviceID")
#             printer_name = run_command("wmic printer get Name")
#             printer_port = run_command("wmic printer get PortName")
#             printer_processor = run_command("wmic printer get PrintProcessor")
#             printer_drivern = run_command("wmic printer get DriverName")

#             # Convert outputs into lists for structured display
#             keyboard_list = keyb_name.splitlines()[1:] if keyb_name else []
#             keyboard_desc_list = keyb_dscp.splitlines()[1:] if keyb_dscp else []
#             keyboard_id_list = keyb_deviceid.splitlines()[1:] if keyb_deviceid else []
#             mouse_list = mouse_name.splitlines()[1:] if mouse_name else []
#             mouse_id_list = mouse_deviceid.splitlines()[1:] if mouse_deviceid else []
#             printer_list = printer_name.splitlines()[1:] if printer_name else []
#             port_list = printer_port.splitlines()[1:] if printer_port else []
#             processor_list = printer_processor.splitlines()[1:] if printer_processor else []
#             driver_list = printer_drivern.splitlines()[1:] if printer_drivern else []

#         else:  # Linux Commands
#             keyboard_list = ["Not Available"]
#             mouse_list = ["Not Available"]
#             printer_list = run_command("lpstat -p").splitlines() if run_command("lpstat -p") else ["Not Available"]

#         return {
#             "Peripherals Info": {
#                 "Keyboard": keyboard_list,
#                 "Keyboard Description": keyboard_desc_list,
#                 "Keyboard DeviceID": keyboard_id_list,
#                 "Mouse": mouse_list,
#                 "Mouse DeviceID": mouse_id_list,
#                 "Printer": printer_list,
#                 "Port Name": port_list,
#                 "Print Processor": processor_list,
#                 "Driver Name": driver_list,
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_software():
#     try:
#         os_type = platform.system()
        
#         if os_type == "Windows":
#             name = run_command("wmic product get Name | findstr /V Name")
#             software_list = name.splitlines() if name else []  # Split by new lines
#         else:  # Linux
#             name = run_command("apt list --installed")
#             software_list = name.splitlines() if name else []

#         # Clean and format the list
#         software_list = [s.strip() for s in software_list if s.strip()]

#         return {
#             "Software Installed": {
#                 "Name": software_list,  # This is now a proper list
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}



# # def index(request):
# #     return render(request, 'index.html')

# def summary(request):
#     return render(request, 'summary.html')

# def os_info(request):
#     return render(request, 'os.html')

# def cpu(request):
#     return render(request, 'cpu.html')

# def motherboard(request):
#     return render(request, 'motherboard.html')

# def gpu(request):
#     return render(request, 'gpu.html')

# def ram(request):
#     return render(request, 'ram.html')

# def storage(request):
#     return render(request, 'storage.html')

# def audio(request):
#     return render(request, 'audio.html')

# def network(request):
#     return render(request, 'network.html')

# def peripherals(request):
#     return render(request, 'peripherals.html')

# def software(request):
#     return render(request, 'software.html')

# def system_info(request):
#     try:
#         refresh = request.GET.get('refresh', 'false').lower() == 'true'
        
#         # Check if cache exists and refresh is not requested
#         if not refresh:
#             cached_data = cache.get('system_info')
#             if cached_data:
#                 return JsonResponse(cached_data)

#         # Fetch new data
#         data = get_os_info()
#         data1 = get_cpu_info()
#         data2 = get_summary()
#         data3 = get_motherboard_info()
#         data4 = get_gpu_info()
#         data5 = get_ram_info()
#         data6 = get_storage_info()
#         data7 = get_audio_info()
#         data8 = get_network_info()
#         data9 = get_peripherals_info()
#         data10 = get_software()
#         combined_data = {**data, **data1, **data2, **data3, **data4, **data5, **data6, **data7, **data8, **data9, **data10}

#         # Store in cache
#         cache.set('system_info', combined_data, timeout=900)

#         return JsonResponse(combined_data)

#     except Exception as e:
#         return JsonResponse({"error": str(e)})








# from django.http import HttpResponseRedirect, JsonResponse
# from django.shortcuts import render, redirect
# from django.core.cache import cache
# from django.contrib import messages
# import platform
# import subprocess
# import re
# from .forms import LoginForm
# import nmap
# import socket
# import paramiko
# import psutil
# from django.shortcuts import render
# import socket
# import sys
# import os
# import json
# import datetime


# def get_client_ip(request):
#     """Retrieve the real client IP address, even behind a proxy."""
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]  # Get the first IP in the list
#     else:
#         ip = request.META.get('REMOTE_ADDR')  # Fallback to standard method
#     return ip

# def view_client_data(request):
#     """Fetch and serve stored system info based on the real client's IP."""
#     client_ip = get_client_ip(request)
#     print(f"📌 Client IP detected: {client_ip}")

#     # Check if a JSON file exists for this client
#     json_path = os.path.join("device_data", f"{client_ip}.json")

#     if os.path.exists(json_path):
#         with open(json_path, "r", encoding="utf-8") as json_file:
#             data = json.load(json_file)
#         return JsonResponse(data)
#     else:
#         return JsonResponse({"error": f"No system info found for your device (IP: {client_ip})"}, status=404)  
    
      
# def get_local_ip():
#     """Get the current device's local IP address."""
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(("8.8.8.8", 80))
#         local_ip = s.getsockname()[0]
#         s.close()
#         return local_ip
#     except socket.error as e:
#         print(f"Error getting local IP: {e}")
#         return "Unknown"

# def check_ssh(ip):
#     """Check if SSH is available on a device."""
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(1)  # Timeout in seconds
#     result = sock.connect_ex((ip, 22))
#     sock.close()
#     return result == 0  # True if SSH is open, False otherwise

# def get_network_devices():
#     """Scan network for all connected devices and check SSH availability."""
#     nm = nmap.PortScanner()
#     local_ip = get_local_ip()
#     network_range = ".".join(local_ip.split(".")[:3]) + ".0/24"  # Example: 192.168.1.0/24

#     try:
#         print(f"Scanning network: {network_range}")  # Debugging log
#         nm.scan(hosts=network_range, arguments="-sn")  # Ping scan (detects all devices)
#         devices = []

#         for host in nm.all_hosts():
#             has_ssh = check_ssh(host)  # Check if SSH is available
#             devices.append({
#                 "ip": host,
#                 "is_self": (host == local_ip),
#                 "has_ssh": has_ssh
#             })

#         print("Detected Devices:", devices)  # Debugging log
#         return devices

#     except Exception as e:
#         print(f"Error scanning network: {e}")
#         return []

# def get_system_info():
#     """Retrieve local system details."""
#     return {
#         "ip": get_local_ip(),
#         "cpu": f"{psutil.cpu_percent()}% CPU usage",
#         "ram": f"{psutil.virtual_memory().percent}% RAM usage",
#         "disk": f"{psutil.disk_usage('/').percent}% Disk usage"
#     }

# def get_network_devices():
#     """Scan network for all connected devices and check SSH availability."""
#     nm = nmap.PortScanner()
#     local_ip = get_local_ip()
#     network_range = "{}.{}.{}.0/24".format(*local_ip.split(".")[:3])

#     try:
#         print(f"Scanning network: {network_range}")
#         nm.scan(hosts=network_range, arguments="-sn")
#         devices = []

#         for host in nm.all_hosts():
#             has_ssh = check_ssh(host)
#             devices.append({"ip": host, "is_self": (host == local_ip), "has_ssh": has_ssh})

#         print("Detected Devices:", devices)
#         return devices
#     except Exception as e:
#         print(f"Error scanning network: {e}")
#         return []


# def get_remote_info(ip, username, password):
#     """Fetch system details from a remote Windows device via SSH."""
#     try:
#         print(f"🔌 Connecting to {ip} via SSH as {username}...")  

#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         client.connect(ip, username=username, password=password, timeout=10)

#         commands = {
#             "OS Info": "wmic os get Caption",
#             "CPU Info": "wmic cpu get Name",
#             "Motherboard Info": "wmic baseboard get Product",
#             "GPU Info": "wmic path win32_videocontroller get Caption",
#             "RAM Info": "wmic memorychip get Capacity",
#             "Storage Info": "wmic logicaldisk get Size",
#             "Audio Info": "wmic sounddev get Caption",
#             "Network Info": "wmic nic where NetEnabled=true get Name",
#             "Peripherals Info": "wmic path Win32_PnPEntity get Name",
#             "Software Installed": "wmic product get Name"
#         }

#         device_info = {"ip": ip}

#         for key, cmd in commands.items():
#             stdin, stdout, stderr = client.exec_command(cmd)
#             # output = stdout.read().decode().strip()
#             # error = stderr.read().decode().strip()
#             output = stdout.read().decode("latin-1").strip()
#             error = stderr.read().decode("latin-1").strip()
#             # output = stdout.read().decode("utf-8", errors="ignore")
#             # error = stderr.read().decode("utf-8", errors="ignore").strip()

            
#             if error:
#                 print(f"⚠️ Command '{cmd}' failed: {error}")
#                 device_info[key] = f"Error: {error}"
#             else:
#                 print(f"✅ {key}: {output}")
#                 device_info[key] = output if output else "N/A"

#         client.close()
#         print(f"✅ Successfully fetched details for {ip}: {device_info}")

#         return device_info

#     except paramiko.AuthenticationException:
#         print(f"❌ Authentication failed for {ip}!")
#         return {"error": "Authentication failed. Please check your username and password."}

#     except paramiko.SSHException as e:
#         print(f"❌ SSH error for {ip}: {e}")
#         return {"error": f"SSH error: {e}"}

#     except Exception as e:
#         print(f"❌ Connection failed for {ip}: {e}")
#         return {"error": f"Failed to fetch remote info: {e}"}


# def device_list(request):
#     """Render a list of detected devices."""
#     devices = get_network_devices()
#     return render(request, "device_list.html", {"devices": devices})


# def device_summary(request, ip):
#     """Fetch and store all system info categories for a device while keeping the HTML view intact."""
#     local_ip = get_local_ip()
#     print(f"🔍 Fetching all system info for device: {ip}")

#     username = request.GET.get("username", "").strip()
#     password = request.GET.get("password", "").strip()

#     print(f"👤 Username: {username}, Password: {'*' * len(password)}")  # Masked password

#     if not username or not password:
#         print("❌ Missing SSH credentials!")
#         return render(request, "summary.html", {"error": "SSH credentials are required!"})

#     if ip == local_ip:
#         print("📌 Fetching LOCAL system info...")
#         data = {
#             "OS": get_os_info(),
#             "CPU": get_cpu_info(),
#             "Motherboard": get_motherboard_info(),
#             "GPU": get_gpu_info(),
#             "RAM": get_ram_info(),
#             "Storage": get_storage_info(),
#             "Audio": get_audio_info(),
#             "Network": get_network_info(),
#             "Peripherals": get_peripherals_info(),
#             "Software": get_software()
#         }
#     else:
#         print(f"🔌 Attempting SSH connection to {ip} as {username}...")
#         device_info = get_remote_info(ip, username=username, password=password)

#         if not device_info or "error" in device_info:
#             print(f"❌ SSH Fetch Failed: {device_info.get('error', 'Unknown error')}")
#             return render(request, "summary.html", {"error": device_info.get("error", "SSH Connection Failed!")})

#         data = {
#             "OS": device_info.get("OS Info", {}),
#             "CPU": device_info.get("CPU Info", {}),
#             "Motherboard": device_info.get("Motherboard Info", {}),
#             "GPU": device_info.get("GPU Info", {}),
#             "RAM": device_info.get("RAM Info", {}),
#             "Storage": device_info.get("Storage Info", {}),
#             "Audio": device_info.get("Audio Info", {}),
#             "Network": device_info.get("Network Info", {}),
#             "Peripherals": device_info.get("Peripherals Info", {}),
#             "Software": device_info.get("Software Installed", {})
#         }

#     json_path = save_device_data(ip, data)
#     print(f"✅ System info stored in: {json_path}")

#     return render(request, "summary.html", {"device_info": data})


# def save_device_data(ip, data):
#     """Helper function to save system info to a JSON file."""

#     os.makedirs("device_data", exist_ok=True)  # Ensure directory exists
#     json_filename = f"{ip}.json"
#     json_path = os.path.join("device_data", json_filename)

#     # Add timestamp
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     data_with_timestamp = {"Last Updated": timestamp, **data}

#     try:
#         # Write JSON data to file
#         with open(json_path, "w", encoding="utf-8") as json_file:
#             json.dump(data_with_timestamp, json_file, indent=4)
        
#         # Verify if the file is written correctly
#         with open(json_path, "r", encoding="utf-8") as json_file:
#             saved_data = json.load(json_file)

#         if not saved_data:
#             print("⚠️ JSON file saved but is empty! Something went wrong.")
#         else:
#             print(f"✅ Data successfully saved at: {json_path} (Updated on: {timestamp})")

#     except Exception as e:
#         print(f"❌ Error saving JSON file: {e}")

#     return json_path


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             serial_no = form.cleaned_data.get('serial_no')
#             password = form.cleaned_data.get('password')
#             # TODO: Implement authentication logic here
#             messages.error(request, 'Invalid credentials')
#             return redirect('device_list')
#             # return redirect('index')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


# def run_command(command):
#     try:
#         # result = subprocess.check_output(command, shell=True, text=True).strip()
#         result = subprocess.check_output(command, shell=True, text=True)
#         return result
#         # return result.strip()
#     except subprocess.CalledProcessError as e:
#         return f"Error: {e}"

# def get_wifi_ipv4():
#     try:
#         # Running ipconfig to get all adapter details
#         ipconfig_output = run_command("ipconfig")

#         # Searching for the "Wireless LAN adapter Wi-Fi" section and the corresponding IPv4 Address
#         wifi_ipv4 = None
#         wifi_section_found = False

#         # Splitting the output into lines to process each line
#         for line in ipconfig_output.splitlines():
#             # Check if the current line is in the Wireless LAN adapter Wi-Fi section
#             if "Wireless LAN adapter Wi-Fi" in line:
#                 wifi_section_found = True
#             elif wifi_section_found and "IPv4 Address" in line:  # Once we find the Wi-Fi section, look for IPv4
#                 match = re.search(r"IPv4 Address(?:[^\r\n]*):\s+([\d.]+)", line)
#                 if match:
#                     wifi_ipv4 = match.group(1)
#                 break  # Stop once we find the IPv4 address
        
#         return wifi_ipv4 if wifi_ipv4 else "Not Available"

#     except Exception as e:
#         return f"Error: {str(e)}"

# def get_summary():
#     try:
#         os_type = platform.system()
#         if os_type == "Windows":
#             os_name = run_command("wmic os get Caption | findstr /V Caption")
#             cpu_name = run_command("wmic cpu get name | findstr /V Name")
#             ram_size = run_command("wmic memorychip get Capacity | findstr /V Capacity")
#             motherboard1 = run_command("wmic baseboard get Manufacturer | findstr /V Manufacturer")
#             motherboard2 = run_command("wmic baseboard get Product | findstr /V Product")
#             graphics = run_command("wmic path Win32_VideoController get Name | findstr /V Name")
#             storage = run_command("wmic diskdrive get Size | findstr /V Size")
#             network = get_wifi_ipv4()
#             audio = run_command("wmic sounddev get Name | findstr /V Name")

#             # Convert RAM size from bytes to GB
#             if ram_size:
#                 size_gb = [f"{int(int(s.strip()) / 1073741824)}GB" for s in ram_size.splitlines() if s.strip().isdigit()]
#                 ram_size = " + ".join(size_gb) if size_gb else "Not Available"
#             else:
#                 ram_size = "Not Available"

#             # Convert storage from bytes to GB (1 GB = 1073741824 bytes)
#             if storage:
#                 storage_gb = [f"{int(int(size.strip()) / 1073741824)}GB" for size in storage.splitlines() if size.strip().isdigit()]
#                 storage = ", ".join(storage_gb) if storage_gb else "Not Available"
#             else:
#                 storage = "Not Available"

#         else:  # Linux Commands
#             os_name = run_command("lsb_release -d | awk -F'\t' '{print $2}'")
            
#         return {
#             "Summary": {
#                 "Operating System": os_name.strip() if os_name else "Not Available",
#                 "CPU": cpu_name.strip() if cpu_name else "Not Available",
#                 "RAM": ram_size,
#                 "Motherboard": f"{motherboard1.strip()} {motherboard2.strip()}".strip() if motherboard1 or motherboard2 else "Not Available",
#                 "Graphics": graphics.strip() if graphics else "Not Available",
#                 "Storage": storage,
#                 "Network": network.strip() if network else "Not Available",
#                 "Audio": audio.strip() if audio else "Not Available",
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}


# def get_os_info():
#     try:
#         os_type = platform.system()

#         if os_type == "Windows":
#             os_name = run_command("wmic os get Caption | findstr /V Caption")
#             os_version = run_command("wmic os get Version | findstr /V Version")
#             os_architecture = run_command("wmic os get OSArchitecture | findstr /V OSArchitecture")
#             wifi_ipv4_address = get_wifi_ipv4()
#             os_manufacturer = run_command("wmic os get Manufacturer | findstr /V Manufacturer")
#             os_serialno = run_command("wmic os get SerialNumber | findstr /V SerialNumber")
#             os_installdate = run_command("wmic os get InstallDate | findstr /V InstallDate")
#             # os_uac_name = run_command("wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName | findstr /V displayName")
#             # os_uac_path = run_command("wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get pathToSignedProductExe | findstr /V pathToSignedProductExe")
#             firewall_name = run_command("wmic service where Name='mpssvc' get Name | findstr /V Name")
#             firewall_startmode = run_command("wmic service where Name='mpssvc' get StartMode | findstr /V StartMode")
#             firewall_status = run_command("wmic service where Name='mpssvc' get State | findstr /V Status")
#             autoupdt_caption = run_command("wmic qfe get Caption | findstr /V Caption")
#             autoupdt_instlledon = run_command("wmic qfe get InstalledOn | findstr /V InstalledOn")
#             autoupdt_hotfixid = run_command("wmic qfe get HotFixID | findstr /V HotFixID")
#             battery_status = run_command("wmic path Win32_Battery get BatteryStatus | findstr /V BatteryStatus")
#             battery_remain = run_command(" wmic path Win32_Battery get EstimatedChargeRemaining | findstr /V EstimatedChargeRemaining")
        
#         else:    #Linux
#             os_name = run_command("lsb_release -d | awk -F'\t' '{print $2}'")

#         return {
#             "OS Info": {
#                 "OS Name": os_name.strip() if os_name else "Not Available",
#                 "OS Version": os_version.strip() if os_version else "Not Available",
#                 "OS Architecture": os_architecture.strip() if os_architecture else "Not Available",
#                 "Wi-Fi IPv4 Address": wifi_ipv4_address,
#                 "Manufacturer": os_manufacturer.strip() if os_manufacturer else "Not Available",
#                 "Serial Number": os_serialno.strip() if os_serialno else "Not Available",
#                 "Install Date": os_installdate.strip() if os_installdate else "Not Available",
#                 # "UAC Name": os_uac_name.strip() if os_uac_name else "Not Available",
#                 # "UAC Path": os_uac_path.strip() if os_uac_path else "Not Available",
#                 "Firewall Name": firewall_name.strip() if firewall_name else "Not Available",
#                 "Firewall StartMode": firewall_startmode.strip() if firewall_startmode else "Not Available",
#                 "Firewall Status": firewall_status.strip() if firewall_status else "Not Available",
#                 "AutoUpdate Caption": autoupdt_caption.strip() if autoupdt_caption else "Not Available",
#                 "AutoUpdate InstalledOn": autoupdt_instlledon.strip() if autoupdt_instlledon else "Not Available",
#                 "AutoUpdate HotFixID": autoupdt_hotfixid.strip() if autoupdt_hotfixid else "Not Available",
#                 "Battery Status": battery_status.strip() if battery_status else "Not Available",
#                 "Charging Remaining": battery_remain.strip() if battery_remain else "Not Available",
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}
    
# def get_cpu_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             cpu_name = run_command("wmic cpu get name | findstr /V Name")
#             cpu_architecture = run_command("wmic cpu get architecture | findstr /V Architecture")
#             cpu_socketdesignation = run_command("wmic cpu get SocketDesignation | findstr /V SocketDesignation")
#             cpu_nocores = run_command("wmic cpu get NumberOfCores | findstr /V NumberOfCores")
#             cpu_logicalproc = run_command("wmic cpu get NumberOfLogicalProcessors | findstr /V NumberOfLogicalProcessors")
#             cpu_frequency = run_command("wmic cpu get CurrentClockSpeed | findstr /V CurrentClockSpeed")
#             cpu_loadper = run_command("wmic cpu get LoadPercentage | findstr /V LoadPercentage")
#             cpu_family = run_command("wmic cpu get Family | findstr /V Family")
#             cpu_descp = run_command("wmic cpu get Description | findstr /V  Description")
#             cpu_processorid = run_command("wmic cpu get ProcessorId | findstr /V ProcessorId")
#             cpu_manufacturer = run_command("wmic cpu get Manufacturer | findstr /V Manufacturer")
#             cpu_deviceid = run_command("wmic cpu get DeviceID | findstr /V DeviceID")
#             cpu_stock = run_command("wmic cpu get MaxClockSpeed | findstr /V MaxClockSpeed")
#             cpu_buspeed = run_command("wmic cpu get ExtClock | findstr /V ExtClock")
#             cpu_vir = run_command("wmic cpu get VirtualizationFirmwareEnabled | findstr /V VirtualizationFirmwareEnabled")
#             cpu_l2 = run_command("wmic cpu get L2CacheSize | findstr /V L2CacheSize")
#             cpu_l3 = run_command("wmic cpu get L3CacheSize | findstr /V L3CacheSize")
#             # cpu_temp = run_command('powershell -Command "((Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace \\"root/wmi\\").CurrentTemperature - 2732) / 10"')

#         else: #Linux
#             cpu_name = run_command("lscpu | grep 'Model name' | awk -F: '{print $2}'")
#             cpu_nocores = run_command("lscpu | grep '^Core(s) per socket' | awk '{print $NF}'")
#             cpu_logicalproc = run_command("nproc")
#             cpu_frequency = run_command("lscpu | grep 'MHz' | awk '{print $NF}'")
#             cpu_manufacturer = run_command("cat /proc/cpuinfo | grep 'vendor_id' | uniq | awk '{print $3}'")

#         return {
#             "CPU Info": {
#                 "CPU Name": cpu_name.strip() if cpu_name else "Not Available",
#                 "CPU Architecture": cpu_architecture.strip() if cpu_architecture else "Not Available",
#                 "Socket Designation": cpu_socketdesignation.strip() if cpu_socketdesignation else "Not Available",
#                 "Number Of Cores" : cpu_nocores.strip() if cpu_nocores else "Not Available",
#                 "Number Of Logical Processors": cpu_logicalproc.strip() if cpu_logicalproc else "Not Available",
#                 "Frequency" : cpu_frequency.strip() if cpu_frequency else "Not Available",
#                 "Load Percentage" : cpu_loadper.strip() if cpu_loadper else "Not Available",
#                 "Description": cpu_descp.strip() if cpu_descp else "Not Available",
#                 "Family": cpu_family.strip() if cpu_family else "Not Available",
#                 "Processor ID": cpu_processorid.strip() if cpu_processorid else "Not Available",
#                 "Manufacturer": cpu_manufacturer.strip() if cpu_manufacturer else "Not Available",
#                 "Device ID": cpu_deviceid.strip() if cpu_deviceid else "Not Available",
#                 "Stock Core Speed": cpu_stock.strip() if cpu_stock else "Not Available",
#                 "Bus Speed": cpu_buspeed.strip() if cpu_buspeed else "Not Available",
#                 "Virtualization": cpu_vir.strip() if cpu_vir else "Not Available",
#                 "L2 Cache Size": cpu_l2.strip() if cpu_l2 else "Not Available",
#                 "L3 Cache Size": cpu_l3.strip() if cpu_l3 else "Not Available",
#                 # "CPU Temperature" : cpu_temp.strip(),
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}


# def get_motherboard_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             motherboard_manufacturer = run_command("wmic baseboard get Manufacturer | findstr /V Manufacturer")
#             motherboard_product = run_command("wmic baseboard get Product | findstr /V Product")
#             motherboard_version = run_command("wmic baseboard get Version | findstr /V Version")
#             motherboard_serial = run_command("wmic baseboard get SerialNumber | findstr /V SerialNumber")
#             bios_manufacturer = run_command("wmic bios get Manufacturer | findstr /V Manufacturer")
#             bios_version = run_command("wmic bios get Version | findstr /V Version")
#             bios_release_date = run_command("wmic bios get ReleaseDate | findstr /V ReleaseDate")
#             memorychip_manufacturer = run_command("wmic memorychip get Manufacturer | findstr /V Manufacturer")
#             memorychip_capacity = run_command("wmic memorychip get Capacity | findstr /V Capacity")
#             memorychip_deviceloc = run_command("wmic memorychip get DeviceLocator | findstr /V DeviceLocator")
#             memorychip_partno = run_command("wmic memorychip get PartNumber | findstr /V PartNumber")
#             memorychip_speed = run_command("wmic memorychip get Speed | findstr /V Speed")
#             memorychip_type = run_command("wmic memorychip get MemoryType | findstr /V MemoryType")
#             usb_name = run_command("wmic path Win32_USBController get Name | findstr /V Name")
#             usb_description = run_command("wmic path Win32_USBHub get Description | findstr /V Description")
#             usb_status = run_command("wmic path Win32_USBController get Status | findstr /V Status")
#             pcie_name = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get Name | findstr /V Name")
#             pcie_deviceid = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get DeviceID | findstr /V DeviceID")
#             pcie_manuf = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get Manufacturer | findstr /V Manufacturer")
#             netadpt_name = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get Name | findstr /V Name")
#             netadpt_netconnid = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get NetConnectionID | findstr /V NetConnectionID")
#             netadpt_adptype = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get AdapterType | findstr /V AdapterType")
#             netadpt_macadd = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get MACAddress | findstr /V MACAddress")
        
#         else:  #Linux
#             motherboard_manufacturer = run_command("sudo dmidecode -t baseboard")

#         return {
#             "Motherboard Info": {
#                 "Manufacturer": motherboard_manufacturer.strip() if motherboard_manufacturer else "Not Available",
#                 "Product": motherboard_product.strip() if motherboard_product else "Not Available",
#                 "Version": motherboard_version.strip() if motherboard_version else "Not Available",
#                 "Serial Number": motherboard_serial.strip() if motherboard_serial else "Not Available",
#                 "Bios Manufacturer": bios_manufacturer.strip() if bios_manufacturer else "Not Available",
#                 "Bios Version": bios_version.strip() if bios_version else "Not Available",
#                 "Bios Release Date": bios_release_date.strip() if bios_release_date else "Not Available",
#                 "Memory Chip Manufacturer" : memorychip_manufacturer.strip() if memorychip_manufacturer else "Not Available",
#                 "Memory Chip Capacity" : memorychip_capacity.strip() if memorychip_capacity else "Not Available",
#                 "Memory Chip Device Locator" : memorychip_deviceloc.strip() if memorychip_deviceloc else "Not Available",
#                 "Memory Chip Part Number" : memorychip_partno.strip() if memorychip_partno else "Not Available",
#                 "Memory Chip Speed" : memorychip_speed.strip() if memorychip_speed else "Not Available",
#                 "Memory Chip Type" : memorychip_type.strip() if memorychip_type else "Not Available",
#                 "USB Name" : usb_name.strip() if usb_name else "Not Available",
#                 "USB Description" : usb_description.strip() if usb_description else "Not Available",
#                 "USB Status" : usb_status.strip() if usb_status else "Not Available",
#                 "PCIe Name" : pcie_name.strip() if pcie_name else "Not Available",
#                 "PCIe Device ID" : pcie_deviceid.strip() if pcie_deviceid else "Not Available",
#                 "PCIe Manufacturer" : pcie_manuf.strip() if pcie_manuf else "Not Available",
#                 "Network Adapter Name" : netadpt_name.strip() if netadpt_name else "Not Available",
#                 "Network Adapter Net Connection ID" : netadpt_netconnid.strip() if netadpt_netconnid else "Not Available",
#                 "Network Adapter Type" : netadpt_adptype.strip() if netadpt_adptype else "Not Available",
#                 "Network Adapter MACAddress" : netadpt_macadd.strip() if netadpt_macadd else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_gpu_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             monitor_caption = run_command("wmic desktopmonitor get Caption | findstr /V Caption")
#             monitor_deviceid = run_command("wmic desktopmonitor get DeviceID | findstr /V DeviceID")
#             monitor_pnpid = run_command("wmic desktopmonitor get PNPDeviceID | findstr /V PNPDeviceID")
#             gpu_name = run_command("wmic path Win32_VideoController get Name | findstr /V Name")
#             gpu_adptcomp = run_command("wmic path Win32_VideoController get AdapterCompatibility | findstr /V AdapterCompatibility")
#             gpu_pnpid = run_command("wmic path Win32_VideoController get PNPDeviceID | findstr /V PNPDeviceID")
#             gpu_vdprocessor = run_command("wmic path Win32_VideoController get VideoProcessor | findstr /V VideoProcessor")
#             gpu_driver = run_command("wmic path Win32_VideoController get DriverVersion | findstr /V DriverVersion")
#             gpu_curr_refreshrate = run_command("wmic path Win32_VideoController get CurrentRefreshRate | findstr /V CurrentRefreshRate")
#             gpu_currhor = run_command("wmic path Win32_VideoController get CurrentHorizontalResolution | findstr /V CurrentHorizontalResolution")
#             gpu_currvert = run_command("wmic path Win32_VideoController get CurrentVerticalResolution | findstr /V CurrentVerticalResolution")
#             gpu_currbits = run_command("wmic path Win32_VideoController get CurrentBitsPerPixel | findstr /V CurrentBitsPerPixel")
#             max_refresh = run_command("wmic path Win32_VideoController get MaxRefreshRate | findstr /V MaxRefreshRate")
#             min_refresh = run_command("wmic path Win32_VideoController get MinRefreshRate | findstr /V MinRefreshRate")
#             video_desp = run_command("wmic path Win32_VideoController get VideoModeDescription | findstr /V VideoModeDescription")
#             curr_nocolor = run_command("wmic path Win32_VideoController get CurrentNumberOfColors | findstr /V CurrentNumberOfColors")
        
#         else:  # For Linux or macOS
#             gpu_name = run_command('sudo lshw -C display')

#         return {
#             "GPU Info": {
#                 "Monitor Caption" : monitor_caption.strip() if monitor_caption else "Not Available",
#                 "Monitor DeviceID" : monitor_deviceid.strip() if monitor_deviceid else "Not Available",
#                 "Monitor PNPDeviceID" : monitor_pnpid.strip() if monitor_pnpid else "Not Available",
#                 "GPU Name" : gpu_name.strip() if gpu_name else "Not Available",
#                 "GPU AdapterCompatibility" : gpu_adptcomp.strip() if gpu_adptcomp else "Not Available",
#                 "GPU PNPDeviceID" : gpu_pnpid.strip() if gpu_pnpid else "Not Available",
#                 "GPU VideoProcessor" : gpu_vdprocessor.strip() if gpu_vdprocessor else "Not Available",
#                 "GPU Driver" : gpu_driver.strip() if gpu_driver else "Not Available",
#                 "GPU CurrentRefreshRate" : gpu_curr_refreshrate.strip() if gpu_curr_refreshrate else "Not Available",
#                 "GPU CurrentHorizontalResolution" : gpu_currhor.strip() if gpu_currhor else "Not Available",
#                 "GPU CurrentVerticalResolution" : gpu_currvert.strip() if gpu_currvert else "Not Available",
#                 "GPU CurrentBitsPerPixel" : gpu_currbits.strip() if gpu_currbits else "Not Available",
#                 "GPU MaxRefreshRate" : max_refresh.strip() if max_refresh else "Not Available",
#                 "GPU MinRefreshRate" : min_refresh.strip() if min_refresh else "Not Available",
#                 "GPU VideoModeDescription" : video_desp.strip() if video_desp else "Not Available",
#                 "GPU CurrentNumberOfColors" : curr_nocolor.strip() if curr_nocolor else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}


# def get_ram_info():
#     try:

#         os_type = platform.system()

#         if os_type == "Windows":
#             physical_memory = run_command("wmic computersystem get TotalPhysicalMemory | findstr /V TotalPhysicalMemory")
#             memory_size = run_command("wmic OS get TotalVisibleMemorySize | findstr /V TotalVisibleMemorySize")
#             free_memory = run_command("wmic OS get FreePhysicalMemory | findstr /V FreePhysicalMemory")
#             total_virtual = run_command("wmic OS get TotalVirtualMemorySize | findstr /V TotalVirtualMemorySize")
#             free_virtual = run_command("wmic OS get FreeVirtualMemory | findstr /V FreeVirtualMemory")
#             capacity = run_command("wmic MemoryChip get Capacity | findstr /V Capacity")
#             memory_Type = run_command("wmic MemoryChip get MemoryType | findstr /V MemoryType")
#             speed = run_command("wmic MemoryChip get Speed | findstr /V  Speed")

#             if physical_memory:
#                 size_gb = [f"{int(int(s.strip()) / 1073741824)}GB" for s in physical_memory.splitlines() if s.strip().isdigit()]
#                 physical_memory = " + ".join(size_gb) if size_gb else "Not Available"
#             else:
#                 physical_memory = "Not Available"
        
#         else:  # For Linux or macOS
#             memory_size = run_command('sudo dmidecode --type memory | grep -i "Size"')

#         return {
#             "RAM Info": {
#                 "TotalPhysicalMemory" : physical_memory.strip() if physical_memory else "Not Available",
#                 "TotalVisibleMemorySize": memory_size.strip() if memory_size else "Not Available",
#                 "FreePhysicalMemory": free_memory.strip() if free_memory else "Not Available",
#                 "TotalVirtualMemorySize": total_virtual.strip() if total_virtual else "Not Available",
#                 "FreeVirtualMemory": free_virtual.strip() if free_virtual else "Not Available",
#                 "Capacity": capacity.strip() if capacity else "Not Available",
#                 "MemoryType": memory_Type.strip() if memory_Type else "Not Available",
#                 "Speed": speed.strip() if speed else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}
    
# def get_storage_info():
#     try:

#         os_type = platform.system()  # Make sure this is set properly

#         if os_type == "Windows":
#             diskdrive_deviceid = run_command("wmic diskdrive get DeviceID | findstr /V DeviceID")
#             diskdrive_model = run_command("wmic diskdrive get Model | findstr /V Model")
#             diskdrive_size = run_command("wmic diskdrive get Size | findstr /V Size")
#             diskdrive_interface = run_command("wmic diskdrive get InterfaceType | findstr /V InterfaceType")
#             diskdrive_status = run_command("wmic diskdrive get Status | findstr /V Status")
#             diskdrive_mediatype = run_command("wmic diskdrive get MediaType | findstr /V MediaType")
#             partition_name = run_command(" wmic partition get Name | findstr /V Name")
#             partition_index = run_command("wmic partition get Index | findstr /V Index")
#             partition_boot = run_command("wmic partition get BootPartition | findstr /V BootPartition")
#             partition_size = run_command("wmic partition get Size | findstr /V Size")
#             logicaldisk_deviceid = run_command("wmic logicaldisk get DeviceID | findstr /V DeviceID")
#             logicaldisk_filesys = run_command(" wmic logicaldisk get FileSystem | findstr /V FileSystem")
#             logicaldisk_size = run_command("wmic logicaldisk get Size | findstr /V Size")
#             logicaldisk_freespace = run_command("wmic logicaldisk get FreeSpace | findstr /V FreeSpace")
#             logicaldisk_volserialno = run_command("wmic logicaldisk get VolumeSerialNumber | findstr /V VolumeSerialNumber")
        
#         else:  # For Linux, using lsblk
#             diskdrive_mediatype = run_command("lsblk -d -o name,rota")

#         return {
#             "Storage Info": {
#                 "Disk Drive Device ID" : diskdrive_deviceid.strip() if diskdrive_deviceid else "Not Available",
#                 "Disk Drive Model" : diskdrive_model.strip() if diskdrive_model else "Not Available",
#                 "Disk Drive Size" : diskdrive_size.strip() if diskdrive_size else "Not Available",
#                 "Disk Drive Interface" : diskdrive_interface.strip() if diskdrive_interface else "Not Available",
#                 "Disk Drive Status" : diskdrive_status.strip() if diskdrive_status else "Not Available",
#                 "Disk Drive Media Type" : diskdrive_mediatype.strip() if diskdrive_mediatype else "Not Available",
#                 "Partition Name" : partition_name.strip() if partition_name else "Not Available",
#                 "Partition Index" : partition_index.strip() if partition_index else "Not Available",
#                 "Partition Boot" : partition_boot.strip() if partition_boot else "Not Available",
#                 "Partition Size" : partition_size.strip() if partition_size else "Not Available",
#                 "Logical Disk Device ID" : logicaldisk_deviceid.strip() if logicaldisk_deviceid else "Not Available",
#                 "Logical Disk File System" : logicaldisk_filesys.strip() if logicaldisk_filesys else "Not Available",
#                 "Logical Disk Size" : logicaldisk_size.strip() if logicaldisk_size else "Not Available",
#                 "Logical Disk Free Space" : logicaldisk_freespace.strip() if logicaldisk_freespace else "Not Available",
#                 "Logical Disk Volume Serial Number" : logicaldisk_volserialno.strip() if logicaldisk_volserialno else "Not Available",
#             }
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_audio_info():
#     try:
#         os_type = platform.system()
        
#         if os_type == "Windows":
#             sound_card = run_command("wmic sounddev get Name | findstr /V Name")
#             playback = run_command('wmic path Win32_PnPEntity where "Name like \'%Audio%\'" get Name | findstr /V Name')
            
#             sound_card_list = sound_card.splitlines() if sound_card else []
#             playback_list = playback.splitlines() if playback else []
        
#         else:  # Linux Commands
#             playback = run_command("aplay -l")
#             playback_list = playback.splitlines() if playback else []
#             sound_card_list = []

#         # Clean up and remove empty lines
#         sound_card_list = [s.strip() for s in sound_card_list if s.strip()]
#         playback_list = [p.strip() for p in playback_list if p.strip()]

#         return {
#             "Audio Info": {
#                 "Sound Card": sound_card_list,  # Returning as a list
#                 "Playback": playback_list,  # Returning as a list
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_network_info():
#     try:
#         os_type = platform.system()
        
#         if os_type == "Windows":
#             internet_name = run_command(" wmic path Win32_NetworkAdapter where \"NetConnectionStatus=2\" get Name | findstr /V Name")
#             internet_connectstatus = run_command(" wmic path Win32_NetworkAdapter where \"NetConnectionStatus=2\" get NetConnectionStatus | findstr /V NetConnectionStatus")
#             networdadpt_name = run_command("wmic nic get Name | findstr /V Name")
#             networkadpt_netenable = run_command("wmic nic get NetEnabled | findstr /V NetEnabled")
#             networkadpt_macaddr = run_command("wmic nic get MACAddress | findstr /V MACAddress")
#             networkadpt_speed = run_command("wmic nic get Speed | findstr /V Speed")
#             networkadpt_adptype = run_command("wmic nic get AdapterType | findstr /V AdapterType")
#             descrp = run_command("wmic path Win32_NetworkAdapterConfiguration get Description | findstr /V Description")
#             ip_addr = run_command("wmic path Win32_NetworkAdapterConfiguration get IPAddress | findstr /V IPAddress")
#             mac_addr = run_command("wmic path Win32_NetworkAdapterConfiguration get MACAddress | findstr /V MACAddress")
#             ip_gateway = run_command("wmic path Win32_NetworkAdapterConfiguration get DefaultIPGateway | findstr /V DefaultIPGateway")
#             dns_server = run_command("wmic path Win32_NetworkAdapterConfiguration get DNSServerSearchOrder | findstr /V DNSServerSearchOrder")
#             dhcp_server = run_command("wmic path Win32_NetworkAdapterConfiguration get DHCPServer | findstr /V DHCPServer")
#             wifi_name = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get Name | findstr /V Name")
#             wifi_macaddr = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get MACAddress | findstr /V MACAddress")
#             wifi_speed = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get Speed | findstr /V Speed")
#             comp_name = run_command("wmic computersystem get Name | findstr /V Name")
#             comp_workgrp = run_command("wmic computersystem get Workgroup | findstr /V Workgroup")

#         else:  # Linux Commands
#             ip_addr = run_command("ip addr show")
            
#         return {
#             "Network Info": {
#                 "Internet Name" : internet_name.strip() if internet_name else "Not Available",
#                 "Internet ConnectStatus" : internet_connectstatus.strip() if internet_connectstatus else "Not Available",
#                 "Network Adapter Name" : networdadpt_name.strip() if networdadpt_name else "Not Available",
#                 "Network Adapter NetEnable" : networkadpt_netenable.strip() if networkadpt_netenable else "Not Available",
#                 "Network Adapter MACAddress" : networkadpt_macaddr.strip() if networkadpt_macaddr else "Not Available",
#                 "Network Adapter Speed" : networkadpt_speed.strip() if networkadpt_speed else "Not Available",
#                 "Network Adapter AdpType" : networkadpt_adptype.strip() if networkadpt_adptype else "Not Available",
#                 "Description" : descrp.strip() if descrp else "Not Available",
#                 "IP Address" : ip_addr.strip() if ip_addr else "Not Available",
#                 "MAC Address" : mac_addr.strip() if mac_addr else "Not Available",
#                 "IP Gateway" : ip_gateway.strip() if ip_gateway else "Not Available",
#                 "DNS Server" : dns_server.strip() if dns_server else "Not Available",
#                 "DHCP Server" : dhcp_server.strip() if dhcp_server else "Not Available",
#                 "Wi-Fi Name" : wifi_name.strip() if wifi_name else "Not Available",
#                 "Wi-Fi MACAddress" : wifi_macaddr.strip() if wifi_macaddr else "Not Available",
#                 "Wi-Fi Speed" : wifi_speed.strip() if wifi_speed else "Not Available",
#                 "Computer Name" : comp_name.strip() if comp_name else "Not Available",
#                 "Computer Workgroup" : comp_workgrp.strip() if comp_workgrp else "Not Available",
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_peripherals_info():
#     try:
#         os_type = platform.system()

#         if os_type == "Windows":
#             keyb_name = run_command("wmic path Win32_Keyboard get Name")
#             keyb_dscp = run_command("wmic path Win32_Keyboard get Description")
#             keyb_deviceid = run_command("wmic path Win32_Keyboard get DeviceID")
#             mouse_name = run_command("wmic path Win32_PointingDevice get Name")
#             mouse_deviceid = run_command("wmic path Win32_PointingDevice get DeviceID")
#             printer_name = run_command("wmic printer get Name")
#             printer_port = run_command("wmic printer get PortName")
#             printer_processor = run_command("wmic printer get PrintProcessor")
#             printer_drivern = run_command("wmic printer get DriverName")

#             # Convert outputs into lists for structured display
#             keyboard_list = keyb_name.splitlines()[1:] if keyb_name else []
#             keyboard_desc_list = keyb_dscp.splitlines()[1:] if keyb_dscp else []
#             keyboard_id_list = keyb_deviceid.splitlines()[1:] if keyb_deviceid else []
#             mouse_list = mouse_name.splitlines()[1:] if mouse_name else []
#             mouse_id_list = mouse_deviceid.splitlines()[1:] if mouse_deviceid else []
#             printer_list = printer_name.splitlines()[1:] if printer_name else []
#             port_list = printer_port.splitlines()[1:] if printer_port else []
#             processor_list = printer_processor.splitlines()[1:] if printer_processor else []
#             driver_list = printer_drivern.splitlines()[1:] if printer_drivern else []

#         else:  # Linux Commands
#             keyboard_list = ["Not Available"]
#             mouse_list = ["Not Available"]
#             printer_list = run_command("lpstat -p").splitlines() if run_command("lpstat -p") else ["Not Available"]

#         return {
#             "Peripherals Info": {
#                 "Keyboard": keyboard_list,
#                 "Keyboard Description": keyboard_desc_list,
#                 "Keyboard DeviceID": keyboard_id_list,
#                 "Mouse": mouse_list,
#                 "Mouse DeviceID": mouse_id_list,
#                 "Printer": printer_list,
#                 "Port Name": port_list,
#                 "Print Processor": processor_list,
#                 "Driver Name": driver_list,
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def get_software():
#     try:
#         os_type = platform.system()
        
#         if os_type == "Windows":
#             name = run_command("wmic product get Name | findstr /V Name")
#             software_list = name.splitlines() if name else []  # Split by new lines
#         else:  # Linux
#             name = run_command("apt list --installed")
#             software_list = name.splitlines() if name else []

#         # Clean and format the list
#         software_list = [s.strip() for s in software_list if s.strip()]

#         return {
#             "Software Installed": {
#                 "Name": software_list,  # This is now a proper list
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}



# # def index(request):
# #     return render(request, 'index.html')

# def summary(request):
#     return render(request, 'summary.html')

# def os_info(request):
#     return render(request, 'os.html')

# def cpu(request):
#     return render(request, 'cpu.html')

# def motherboard(request):
#     return render(request, 'motherboard.html')

# def gpu(request):
#     return render(request, 'gpu.html')

# def ram(request):
#     return render(request, 'ram.html')

# def storage(request):
#     return render(request, 'storage.html')

# def audio(request):
#     return render(request, 'audio.html')

# def network(request):
#     return render(request, 'network.html')

# def peripherals(request):
#     return render(request, 'peripherals.html')

# def software(request):
#     return render(request, 'software.html')

# def system_info(request):
#     try:
#         refresh = request.GET.get('refresh', 'false').lower() == 'true'
        
#         # Check if cache exists and refresh is not requested
#         if not refresh:
#             cached_data = cache.get('system_info')
#             if cached_data:
#                 return JsonResponse(cached_data)

#         # Fetch new data
#         data = get_os_info()
#         data1 = get_cpu_info()
#         data2 = get_summary()
#         data3 = get_motherboard_info()
#         data4 = get_gpu_info()
#         data5 = get_ram_info()
#         data6 = get_storage_info()
#         data7 = get_audio_info()
#         data8 = get_network_info()
#         data9 = get_peripherals_info()
#         data10 = get_software()
#         combined_data = {**data, **data1, **data2, **data3, **data4, **data5, **data6, **data7, **data8, **data9, **data10}

#         # Store in cache
#         cache.set('system_info', combined_data, timeout=900)

#         return JsonResponse(combined_data)

#     except Exception as e:
#         return JsonResponse({"error": str(e)})













from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import SSHCredential
import platform
import subprocess
import re
from .forms import LoginForm
import nmap
import socket
import paramiko
import psutil
from django.shortcuts import render
import socket
import sys
import os
import json
import datetime



def get_client_ip(request):
    """Retrieve the real client IP address, even behind a proxy."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get the first IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')  # Fallback to standard method
    return ip


def view_client_data(request):
    """Fetch and serve stored system info based on the real client's IP."""
    client_ip = get_client_ip(request)
    print(f"📌 Client IP detected: {client_ip}")

    # Check if a JSON file exists for this client
    json_path = os.path.join("device_data", f"{client_ip}.json")

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return JsonResponse(data)
    else:
        return JsonResponse({"error": f"No system info found for your device (IP: {client_ip})"}, status=404)  
    

def get_local_ip():
    """Get the current device's local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error as e:
        print(f"Error getting local IP: {e}")
        return "Unknown"

def check_ssh(ip):
    """Check if SSH is available on a device."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout in seconds
    result = sock.connect_ex((ip, 22))
    sock.close()
    return result == 0  # True if SSH is open, False otherwise

def get_network_devices():
    """Scan network for all connected devices and check SSH availability."""
    nm = nmap.PortScanner()
    local_ip = get_local_ip()
    network_range = ".".join(local_ip.split(".")[:3]) + ".0/24"  # Example: 192.168.1.0/24

    try:
        print(f"Scanning network: {network_range}")  # Debugging log
        nm.scan(hosts=network_range, arguments="-sn")  # Ping scan (detects all devices)
        devices = []

        for host in nm.all_hosts():
            has_ssh = check_ssh(host)  # Check if SSH is available
            devices.append({
                "ip": host,
                "is_self": (host == local_ip),
                "has_ssh": has_ssh
            })

        print("Detected Devices:", devices)  # Debugging log
        return devices

    except Exception as e:
        print(f"Error scanning network: {e}")
        return []

def get_system_info():
    """Retrieve local system details."""
    return {
        "ip": get_local_ip(),
        "cpu": f"{psutil.cpu_percent()}% CPU usage",
        "ram": f"{psutil.virtual_memory().percent}% RAM usage",
        "disk": f"{psutil.disk_usage('/').percent}% Disk usage"
    }

def get_network_devices():
    """Scan network for all connected devices and check SSH availability."""
    nm = nmap.PortScanner()
    local_ip = get_local_ip()
    network_range = "{}.{}.{}.0/24".format(*local_ip.split(".")[:3])

    try:
        print(f"Scanning network: {network_range}")
        nm.scan(hosts=network_range, arguments="-sn")
        devices = []

        for host in nm.all_hosts():
            has_ssh = check_ssh(host)
            devices.append({"ip": host, "is_self": (host == local_ip), "has_ssh": has_ssh})

        print("Detected Devices:", devices)
        return devices
    except Exception as e:
        print(f"Error scanning network: {e}")
        return []


def get_remote_info(ip, username, password):
    """Fetch system details from a remote Windows device via SSH."""
    try:
        print(f"🔌 Connecting to {ip} via SSH as {username}...")  

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, timeout=10)
        
        commands = {
            "Summary": "wmic computersystem get model",
            "OS Info": "wmic os get caption",
            "CPU Info": "wmic cpu get Name",
            "Motherboard Info": "wmic baseboard get product",
            "GPU Info": "wmic path win32_videocontroller get Caption",
            "RAM Info": "wmic memorychip get Capacity",
            "Storage Info": "wmic logicaldisk get Size",
            "Audio Info": "wmic sounddev get Caption",
            "Network Info": "wmic nic where NetEnabled=true get Name",
            "Peripherals Info": "wmic path Win32_PnPEntity get Name",
            "Software Installed": "wmic product get Name"
        }

        device_info = {"ip": ip}

        for key, cmd in commands.items():
            stdin, stdout, stderr = client.exec_command(cmd)
            # output = stdout.read().decode().strip()
            # error = stderr.read().decode().strip()
            output = stdout.read().decode("latin-1").strip()
            error = stderr.read().decode("latin-1").strip()
            # output = stdout.read().decode("utf-8", errors="ignore")
            # error = stderr.read().decode("utf-8", errors="ignore").strip()

            
            if error:
                print(f"⚠ Command '{cmd}' failed: {error}")
                device_info[key] = f"Error: {error}"
            else:
                # print(f"✅ {key}: {output}")
                # device_info[key] = output if output else "N/A"
                clean_output = [line.strip() for line in output.split("\n") if line.strip()]
                # device_info[key] = clean_output if clean_output else ["N/A"]
                device_info[key] = clean_output[1:] if len(clean_output) > 1 else ["N/A"]

        client.close()
        print(f"✅ Successfully fetched details for {ip}: {device_info}")

        return device_info

    except paramiko.AuthenticationException:
        print(f"❌ Authentication failed for {ip}!")
        return {"error": "Authentication failed. Please check your username and password."}

    except paramiko.SSHException as e:
        print(f"❌ SSH error for {ip}: {e}")
        return {"error": f"SSH error: {e}"}

    except Exception as e:
        print(f"❌ Connection failed for {ip}: {e}")
        return {"error": f"Failed to fetch remote info: {e}"}
    
def device_list(request):
    """Render a list of detected devices."""
    devices = get_network_devices()
    return render(request, "device_list.html", {"devices": devices})

def get_ips(request, serial_no):
    try:
        devices = get_network_devices()
        device = next((d for d in devices if d['serial_no'] == serial_no), None)
        if device:
            return JsonResponse({'ips': device['ip_addresses']})
        else:
            return JsonResponse({'error': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_device_info(request, ip):
    try:
        devices = get_network_devices()
        device = next((d for d in devices if ip in d['ip_addresses']), None)
        if device:
            info = {
                'CPU': device['cpu_info'],
                'RAM': device['ram_info'],
                'OS': device['os_info']
            }
            return JsonResponse({'info': info})
        else:
            return JsonResponse({'error': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


DEVICE_DATA_DIR = os.path.join(os.path.dirname(__file__), 'device_data')

def device_summary(request, ip):
    local_ip = get_local_ip()
    print(f"🔍 Fetching system info for device: {ip}")

    username = request.GET.get("username", "").strip()
    password = request.GET.get("password", "").strip()

    if not username or not password:
        print("❌ Missing SSH credentials!")
        error_msg = "SSH credentials are required!"
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": error_msg}, status=400)
        return render(request, "summary.html", {"error": error_msg})

    json_path = os.path.join(DEVICE_DATA_DIR, f"{ip}.json")

    # Try loading from file
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        print("📁 Loaded existing data from JSON.")
    else:
        if ip == local_ip:
            print("📌 Fetching LOCAL system info...")
            data = {
                "Summary" : get_summary(),
                "OS": get_os_info(),
                "CPU": get_cpu_info(),
                "Motherboard": get_motherboard_info(),
                "GPU": get_gpu_info(),
                "RAM": get_ram_info(),
                "Storage": get_storage_info(),
                "Audio": get_audio_info(),
                "Network": get_network_info(),
                "Peripherals": get_peripherals_info(),
                "Software": get_software()
            }
        else:
            print(f"🔌 Attempting SSH connection to {ip} as {username}...")
            device_info = get_remote_info(ip, username=username, password=password)

            if not device_info or "error" in device_info:
                error_msg = device_info.get("error", "SSH Connection Failed!")
                print(f"❌ SSH Fetch Failed: {error_msg}")
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"error": error_msg}, status=500)
                return render(request, "summary.html", {"error": error_msg})

            data = {
                "Summary": {"Model": device_info.get("Summary", ["N/A"])[0]},
                "OS": {"Name": device_info.get("OS Info", ["N/A"])[0]},
                "CPU": {"Model": device_info.get("CPU Info", ["N/A"])[0]},
                "Motherboard": {"Product": device_info.get("Motherboard Info", ["N/A"])[0]},
                "GPU": {"Model": device_info.get("GPU Info", ["N/A"])[0]},
                "RAM": {"Capacity": device_info.get("RAM Info", ["N/A"])},
                "Storage": {"Size": device_info.get("Storage Info", ["N/A"])},
                "Audio": {"Devices": device_info.get("Audio Info", ["N/A"])},
                "Network": {"Interfaces": device_info.get("Network Info", ["N/A"])},
                "Peripherals": {"Connected": device_info.get("Peripherals Info", ["N/A"])},
                "Software": {"Installed": device_info.get("Software Installed", ["N/A"])}
            }
        # Save fetched data
        save_device_data(ip, data)
        print(f"✅ System info stored in: {json_path}")

    # Respond based on request type
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(data)
    else:
        return render(request, "summary.html", {"device_info": data})


def save_device_data(ip, data):
    """Helper function to save system info to a JSON file with consistent formatting."""
    
    os.makedirs("device_data", exist_ok=True)  # Ensure directory exists
    json_filename = f"{ip}.json"
    json_path = os.path.join("device_data", json_filename)

    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # data_with_timestamp = {"Last Updated": timestamp, **data}
    # Ensure all values are stored as dictionaries
    formatted_data = {
        key: value if isinstance(value, dict) else {"Value": value}
        for key, value in data.items()
    }
    data_with_timestamp = {"Last Updated": timestamp, **formatted_data}
    try:
        # Write JSON data to file
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data_with_timestamp, json_file, indent=4, ensure_ascii=False)
        
        print(f"✅ Data successfully saved at: {json_path} (Updated on: {timestamp})")

    except Exception as e:
        print(f"❌ Error saving JSON file: {e}")

    return json_path


def fetch_remote_device_info(request, ip):
    if request.method == 'POST':
        import json, os
        from django.http import JsonResponse

        try:
            creds = json.loads(request.body)
            username = creds.get("username")
            password = creds.get("password")

            # Use your SSH logic here to fetch data from remote system
            # For now, just return dummy
            json_path = os.path.join('device_data', f'{ip}.json')
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                return JsonResponse(data)

            # Else fetch via SSH (replace this with actual logic)
            data = {"ip": ip, "info": "SSH system info retrieved"}
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=4)

            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            serial_no = form.cleaned_data.get('serial_no')
            password = form.cleaned_data.get('password')
            # TODO: Implement authentication logic here
            messages.error(request, 'Invalid credentials')
            return redirect('device_list')
            # return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def run_command(command):
    try:
        # result = subprocess.check_output(command, shell=True, text=True).strip()
        result = subprocess.check_output(command, shell=True, text=True)
        return result
        # return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def get_wifi_ipv4():
    try:
        # Running ipconfig to get all adapter details
        ipconfig_output = run_command("ipconfig")

        # Searching for the "Wireless LAN adapter Wi-Fi" section and the corresponding IPv4 Address
        wifi_ipv4 = None
        wifi_section_found = False

        # Splitting the output into lines to process each line
        for line in ipconfig_output.splitlines():
            # Check if the current line is in the Wireless LAN adapter Wi-Fi section
            if "Wireless LAN adapter Wi-Fi" in line:
                wifi_section_found = True
            elif wifi_section_found and "IPv4 Address" in line:  # Once we find the Wi-Fi section, look for IPv4
                match = re.search(r"IPv4 Address(?:[^\r\n]*):\s+([\d.]+)", line)
                if match:
                    wifi_ipv4 = match.group(1)
                break  # Stop once we find the IPv4 address
        
        return wifi_ipv4 if wifi_ipv4 else "Not Available"

    except Exception as e:
        return f"Error: {str(e)}"


def get_summary():
    try:
        os_type = platform.system()
        if os_type == "Windows":
            os_name = run_command("wmic os get Caption | findstr /V Caption")
            cpu_name = run_command("wmic cpu get name | findstr /V Name")
            ram_size = run_command("wmic memorychip get Capacity | findstr /V Capacity")
            motherboard1 = run_command("wmic baseboard get Manufacturer | findstr /V Manufacturer")
            motherboard2 = run_command("wmic baseboard get Product | findstr /V Product")
            graphics = run_command("wmic path Win32_VideoController get Name | findstr /V Name")
            storage = run_command("wmic diskdrive get Size | findstr /V Size")
            network = get_wifi_ipv4()
            audio = run_command("wmic sounddev get Name | findstr /V Name")

            # Convert RAM size from bytes to GB
            if ram_size:
                size_gb = [f"{int(int(s.strip()) / 1073741824)}GB" for s in ram_size.splitlines() if s.strip().isdigit()]
                ram_size = " + ".join(size_gb) if size_gb else "Not Available"
            else:
                ram_size = "Not Available"

            # Convert storage from bytes to GB (1 GB = 1073741824 bytes)
            if storage:
                storage_gb = [f"{int(int(size.strip()) / 1073741824)}GB" for size in storage.splitlines() if size.strip().isdigit()]
                storage = ", ".join(storage_gb) if storage_gb else "Not Available"
            else:
                storage = "Not Available"

        else:  # Linux Commands
            os_name = run_command("lsb_release -d | awk -F'\t' '{print $2}'")
            
        return {
            "Summary": {
                "Operating System": os_name.strip() if os_name else "Not Available",
                "CPU": cpu_name.strip() if cpu_name else "Not Available",
                "RAM": ram_size,
                "Motherboard": f"{motherboard1.strip()} {motherboard2.strip()}".strip() if motherboard1 or motherboard2 else "Not Available",
                "Graphics": graphics.strip() if graphics else "Not Available",
                "Storage": storage,
                "Network": network.strip() if network else "Not Available",
                "Audio": audio.strip() if audio else "Not Available",
            },
        }
    except Exception as e:
        return {"error": str(e)}



def get_os_info():
    try:
        os_type = platform.system()

        if os_type == "Windows":
            os_name = run_command("wmic os get Caption | findstr /V Caption")
            os_version = run_command("wmic os get Version | findstr /V Version")
            os_architecture = run_command("wmic os get OSArchitecture | findstr /V OSArchitecture")
            wifi_ipv4_address = get_wifi_ipv4()
            os_manufacturer = run_command("wmic os get Manufacturer | findstr /V Manufacturer")
            os_serialno = run_command("wmic os get SerialNumber | findstr /V SerialNumber")
            os_installdate = run_command("wmic os get InstallDate | findstr /V InstallDate")
            # os_uac_name = run_command("wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName | findstr /V displayName")
            # os_uac_path = run_command("wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get pathToSignedProductExe | findstr /V pathToSignedProductExe")
            firewall_name = run_command("wmic service where Name='mpssvc' get Name | findstr /V Name")
            firewall_startmode = run_command("wmic service where Name='mpssvc' get StartMode | findstr /V StartMode")
            firewall_status = run_command("wmic service where Name='mpssvc' get State | findstr /V Status")
            autoupdt_caption = run_command("wmic qfe get Caption | findstr /V Caption")
            autoupdt_instlledon = run_command("wmic qfe get InstalledOn | findstr /V InstalledOn")
            autoupdt_hotfixid = run_command("wmic qfe get HotFixID | findstr /V HotFixID")
            battery_status = run_command("wmic path Win32_Battery get BatteryStatus | findstr /V BatteryStatus")
            battery_remain = run_command(" wmic path Win32_Battery get EstimatedChargeRemaining | findstr /V EstimatedChargeRemaining")
        
        else:    #Linux
            os_name = run_command("lsb_release -d | awk -F'\t' '{print $2}'")

        return {
            "OS Info": {
                "OS Name": os_name.strip() if os_name else "Not Available",
                "OS Version": os_version.strip() if os_version else "Not Available",
                "OS Architecture": os_architecture.strip() if os_architecture else "Not Available",
                "Wi-Fi IPv4 Address": wifi_ipv4_address,
                "Manufacturer": os_manufacturer.strip() if os_manufacturer else "Not Available",
                "Serial Number": os_serialno.strip() if os_serialno else "Not Available",
                "Install Date": os_installdate.strip() if os_installdate else "Not Available",
                # "UAC Name": os_uac_name.strip() if os_uac_name else "Not Available",
                # "UAC Path": os_uac_path.strip() if os_uac_path else "Not Available",
                "Firewall Name": firewall_name.strip() if firewall_name else "Not Available",
                "Firewall StartMode": firewall_startmode.strip() if firewall_startmode else "Not Available",
                "Firewall Status": firewall_status.strip() if firewall_status else "Not Available",
                "AutoUpdate Caption": autoupdt_caption.strip() if autoupdt_caption else "Not Available",
                "AutoUpdate InstalledOn": autoupdt_instlledon.strip() if autoupdt_instlledon else "Not Available",
                "AutoUpdate HotFixID": autoupdt_hotfixid.strip() if autoupdt_hotfixid else "Not Available",
                "Battery Status": battery_status.strip() if battery_status else "Not Available",
                "Charging Remaining": battery_remain.strip() if battery_remain else "Not Available",
            },
        }
    except Exception as e:
        return {"error": str(e)}
    
    
    
def get_cpu_info():
    try:

        os_type = platform.system()

        if os_type == "Windows":
            cpu_name = run_command("wmic cpu get name | findstr /V Name")
            cpu_architecture = run_command("wmic cpu get architecture | findstr /V Architecture")
            cpu_socketdesignation = run_command("wmic cpu get SocketDesignation | findstr /V SocketDesignation")
            cpu_nocores = run_command("wmic cpu get NumberOfCores | findstr /V NumberOfCores")
            cpu_logicalproc = run_command("wmic cpu get NumberOfLogicalProcessors | findstr /V NumberOfLogicalProcessors")
            cpu_frequency = run_command("wmic cpu get CurrentClockSpeed | findstr /V CurrentClockSpeed")
            cpu_loadper = run_command("wmic cpu get LoadPercentage | findstr /V LoadPercentage")
            cpu_family = run_command("wmic cpu get Family | findstr /V Family")
            cpu_descp = run_command("wmic cpu get Description | findstr /V  Description")
            cpu_processorid = run_command("wmic cpu get ProcessorId | findstr /V ProcessorId")
            cpu_manufacturer = run_command("wmic cpu get Manufacturer | findstr /V Manufacturer")
            cpu_deviceid = run_command("wmic cpu get DeviceID | findstr /V DeviceID")
            cpu_stock = run_command("wmic cpu get MaxClockSpeed | findstr /V MaxClockSpeed")
            cpu_buspeed = run_command("wmic cpu get ExtClock | findstr /V ExtClock")
            cpu_vir = run_command("wmic cpu get VirtualizationFirmwareEnabled | findstr /V VirtualizationFirmwareEnabled")
            cpu_l2 = run_command("wmic cpu get L2CacheSize | findstr /V L2CacheSize")
            cpu_l3 = run_command("wmic cpu get L3CacheSize | findstr /V L3CacheSize")
            # cpu_temp = run_command('powershell -Command "((Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace \\"root/wmi\\").CurrentTemperature - 2732) / 10"')

        else: #Linux
            cpu_name = run_command("lscpu | grep 'Model name' | awk -F: '{print $2}'")
            cpu_nocores = run_command("lscpu | grep '^Core(s) per socket' | awk '{print $NF}'")
            cpu_logicalproc = run_command("nproc")
            cpu_frequency = run_command("lscpu | grep 'MHz' | awk '{print $NF}'")
            cpu_manufacturer = run_command("cat /proc/cpuinfo | grep 'vendor_id' | uniq | awk '{print $3}'")

        return {
            "CPU Info": {
                "CPU Name": cpu_name.strip() if cpu_name else "Not Available",
                "CPU Architecture": cpu_architecture.strip() if cpu_architecture else "Not Available",
                "Socket Designation": cpu_socketdesignation.strip() if cpu_socketdesignation else "Not Available",
                "Number Of Cores" : cpu_nocores.strip() if cpu_nocores else "Not Available",
                "Number Of Logical Processors": cpu_logicalproc.strip() if cpu_logicalproc else "Not Available",
                "Frequency" : cpu_frequency.strip() if cpu_frequency else "Not Available",
                "Load Percentage" : cpu_loadper.strip() if cpu_loadper else "Not Available",
                "Description": cpu_descp.strip() if cpu_descp else "Not Available",
                "Family": cpu_family.strip() if cpu_family else "Not Available",
                "Processor ID": cpu_processorid.strip() if cpu_processorid else "Not Available",
                "Manufacturer": cpu_manufacturer.strip() if cpu_manufacturer else "Not Available",
                "Device ID": cpu_deviceid.strip() if cpu_deviceid else "Not Available",
                "Stock Core Speed": cpu_stock.strip() if cpu_stock else "Not Available",
                "Bus Speed": cpu_buspeed.strip() if cpu_buspeed else "Not Available",
                "Virtualization": cpu_vir.strip() if cpu_vir else "Not Available",
                "L2 Cache Size": cpu_l2.strip() if cpu_l2 else "Not Available",
                "L3 Cache Size": cpu_l3.strip() if cpu_l3 else "Not Available",
                # "CPU Temperature" : cpu_temp.strip(),
            },
        }
    except Exception as e:
        return {"error": str(e)}



def get_motherboard_info():
    try:

        os_type = platform.system()

        if os_type == "Windows":
            motherboard_manufacturer = run_command("wmic baseboard get Manufacturer | findstr /V Manufacturer")
            motherboard_product = run_command("wmic baseboard get Product | findstr /V Product")
            motherboard_version = run_command("wmic baseboard get Version | findstr /V Version")
            motherboard_serial = run_command("wmic baseboard get SerialNumber | findstr /V SerialNumber")
            bios_manufacturer = run_command("wmic bios get Manufacturer | findstr /V Manufacturer")
            bios_version = run_command("wmic bios get Version | findstr /V Version")
            bios_release_date = run_command("wmic bios get ReleaseDate | findstr /V ReleaseDate")
            memorychip_manufacturer = run_command("wmic memorychip get Manufacturer | findstr /V Manufacturer")
            memorychip_capacity = run_command("wmic memorychip get Capacity | findstr /V Capacity")
            memorychip_deviceloc = run_command("wmic memorychip get DeviceLocator | findstr /V DeviceLocator")
            memorychip_partno = run_command("wmic memorychip get PartNumber | findstr /V PartNumber")
            memorychip_speed = run_command("wmic memorychip get Speed | findstr /V Speed")
            memorychip_type = run_command("wmic memorychip get MemoryType | findstr /V MemoryType")
            usb_name = run_command("wmic path Win32_USBController get Name | findstr /V Name")
            usb_description = run_command("wmic path Win32_USBHub get Description | findstr /V Description")
            usb_status = run_command("wmic path Win32_USBController get Status | findstr /V Status")
            pcie_name = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get Name | findstr /V Name")
            pcie_deviceid = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get DeviceID | findstr /V DeviceID")
            pcie_manuf = run_command("wmic path Win32_PnPEntity where \"DeviceID like 'PCI%'\" get Manufacturer | findstr /V Manufacturer")
            netadpt_name = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get Name | findstr /V Name")
            netadpt_netconnid = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get NetConnectionID | findstr /V NetConnectionID")
            netadpt_adptype = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get AdapterType | findstr /V AdapterType")
            netadpt_macadd = run_command("wmic path Win32_NetworkAdapter where \"NetConnectionID is not NULL\" get MACAddress | findstr /V MACAddress")
        
        else:  #Linux
            motherboard_manufacturer = run_command("sudo dmidecode -t baseboard")

        return {
            "Motherboard Info": {
                "Manufacturer": motherboard_manufacturer.strip() if motherboard_manufacturer else "Not Available",
                "Product": motherboard_product.strip() if motherboard_product else "Not Available",
                "Version": motherboard_version.strip() if motherboard_version else "Not Available",
                "Serial Number": motherboard_serial.strip() if motherboard_serial else "Not Available",
                "Bios Manufacturer": bios_manufacturer.strip() if bios_manufacturer else "Not Available",
                "Bios Version": bios_version.strip() if bios_version else "Not Available",
                "Bios Release Date": bios_release_date.strip() if bios_release_date else "Not Available",
                "Memory Chip Manufacturer" : memorychip_manufacturer.strip() if memorychip_manufacturer else "Not Available",
                "Memory Chip Capacity" : memorychip_capacity.strip() if memorychip_capacity else "Not Available",
                "Memory Chip Device Locator" : memorychip_deviceloc.strip() if memorychip_deviceloc else "Not Available",
                "Memory Chip Part Number" : memorychip_partno.strip() if memorychip_partno else "Not Available",
                "Memory Chip Speed" : memorychip_speed.strip() if memorychip_speed else "Not Available",
                "Memory Chip Type" : memorychip_type.strip() if memorychip_type else "Not Available",
                "USB Name" : usb_name.strip() if usb_name else "Not Available",
                "USB Description" : usb_description.strip() if usb_description else "Not Available",
                "USB Status" : usb_status.strip() if usb_status else "Not Available",
                "PCIe Name" : pcie_name.strip() if pcie_name else "Not Available",
                "PCIe Device ID" : pcie_deviceid.strip() if pcie_deviceid else "Not Available",
                "PCIe Manufacturer" : pcie_manuf.strip() if pcie_manuf else "Not Available",
                "Network Adapter Name" : netadpt_name.strip() if netadpt_name else "Not Available",
                "Network Adapter Net Connection ID" : netadpt_netconnid.strip() if netadpt_netconnid else "Not Available",
                "Network Adapter Type" : netadpt_adptype.strip() if netadpt_adptype else "Not Available",
                "Network Adapter MACAddress" : netadpt_macadd.strip() if netadpt_macadd else "Not Available",
            }
        }
    except Exception as e:
        return {"error": str(e)}



def get_gpu_info():
    try:

        os_type = platform.system()

        if os_type == "Windows":
            monitor_caption = run_command("wmic desktopmonitor get Caption | findstr /V Caption")
            monitor_deviceid = run_command("wmic desktopmonitor get DeviceID | findstr /V DeviceID")
            monitor_pnpid = run_command("wmic desktopmonitor get PNPDeviceID | findstr /V PNPDeviceID")
            gpu_name = run_command("wmic path Win32_VideoController get Name | findstr /V Name")
            gpu_adptcomp = run_command("wmic path Win32_VideoController get AdapterCompatibility | findstr /V AdapterCompatibility")
            gpu_pnpid = run_command("wmic path Win32_VideoController get PNPDeviceID | findstr /V PNPDeviceID")
            gpu_vdprocessor = run_command("wmic path Win32_VideoController get VideoProcessor | findstr /V VideoProcessor")
            gpu_driver = run_command("wmic path Win32_VideoController get DriverVersion | findstr /V DriverVersion")
            gpu_curr_refreshrate = run_command("wmic path Win32_VideoController get CurrentRefreshRate | findstr /V CurrentRefreshRate")
            gpu_currhor = run_command("wmic path Win32_VideoController get CurrentHorizontalResolution | findstr /V CurrentHorizontalResolution")
            gpu_currvert = run_command("wmic path Win32_VideoController get CurrentVerticalResolution | findstr /V CurrentVerticalResolution")
            gpu_currbits = run_command("wmic path Win32_VideoController get CurrentBitsPerPixel | findstr /V CurrentBitsPerPixel")
            max_refresh = run_command("wmic path Win32_VideoController get MaxRefreshRate | findstr /V MaxRefreshRate")
            min_refresh = run_command("wmic path Win32_VideoController get MinRefreshRate | findstr /V MinRefreshRate")
            video_desp = run_command("wmic path Win32_VideoController get VideoModeDescription | findstr /V VideoModeDescription")
            curr_nocolor = run_command("wmic path Win32_VideoController get CurrentNumberOfColors | findstr /V CurrentNumberOfColors")
        
        else:  # For Linux or macOS
            gpu_name = run_command('sudo lshw -C display')

        return {
            "GPU Info": {
                "Monitor Caption" : monitor_caption.strip() if monitor_caption else "Not Available",
                "Monitor DeviceID" : monitor_deviceid.strip() if monitor_deviceid else "Not Available",
                "Monitor PNPDeviceID" : monitor_pnpid.strip() if monitor_pnpid else "Not Available",
                "GPU Name" : gpu_name.strip() if gpu_name else "Not Available",
                "GPU AdapterCompatibility" : gpu_adptcomp.strip() if gpu_adptcomp else "Not Available",
                "GPU PNPDeviceID" : gpu_pnpid.strip() if gpu_pnpid else "Not Available",
                "GPU VideoProcessor" : gpu_vdprocessor.strip() if gpu_vdprocessor else "Not Available",
                "GPU Driver" : gpu_driver.strip() if gpu_driver else "Not Available",
                "GPU CurrentRefreshRate" : gpu_curr_refreshrate.strip() if gpu_curr_refreshrate else "Not Available",
                "GPU CurrentHorizontalResolution" : gpu_currhor.strip() if gpu_currhor else "Not Available",
                "GPU CurrentVerticalResolution" : gpu_currvert.strip() if gpu_currvert else "Not Available",
                "GPU CurrentBitsPerPixel" : gpu_currbits.strip() if gpu_currbits else "Not Available",
                "GPU MaxRefreshRate" : max_refresh.strip() if max_refresh else "Not Available",
                "GPU MinRefreshRate" : min_refresh.strip() if min_refresh else "Not Available",
                "GPU VideoModeDescription" : video_desp.strip() if video_desp else "Not Available",
                "GPU CurrentNumberOfColors" : curr_nocolor.strip() if curr_nocolor else "Not Available",
            }
        }
    except Exception as e:
        return {"error": str(e)}


def get_ram_info():
    try:

        os_type = platform.system()

        if os_type == "Windows":
            physical_memory = run_command("wmic computersystem get TotalPhysicalMemory | findstr /V TotalPhysicalMemory")
            memory_size = run_command("wmic OS get TotalVisibleMemorySize | findstr /V TotalVisibleMemorySize")
            free_memory = run_command("wmic OS get FreePhysicalMemory | findstr /V FreePhysicalMemory")
            total_virtual = run_command("wmic OS get TotalVirtualMemorySize | findstr /V TotalVirtualMemorySize")
            free_virtual = run_command("wmic OS get FreeVirtualMemory | findstr /V FreeVirtualMemory")
            capacity = run_command("wmic MemoryChip get Capacity | findstr /V Capacity")
            memory_Type = run_command("wmic MemoryChip get MemoryType | findstr /V MemoryType")
            speed = run_command("wmic MemoryChip get Speed | findstr /V  Speed")

            if physical_memory:
                size_gb = [f"{int(int(s.strip()) / 1073741824)}GB" for s in physical_memory.splitlines() if s.strip().isdigit()]
                physical_memory = " + ".join(size_gb) if size_gb else "Not Available"
            else:
                physical_memory = "Not Available"
        
        else:  # For Linux or macOS
            memory_size = run_command('sudo dmidecode --type memory | grep -i "Size"')

        return {
            "RAM Info": {
                "TotalPhysicalMemory" : physical_memory.strip() if physical_memory else "Not Available",
                "TotalVisibleMemorySize": memory_size.strip() if memory_size else "Not Available",
                "FreePhysicalMemory": free_memory.strip() if free_memory else "Not Available",
                "TotalVirtualMemorySize": total_virtual.strip() if total_virtual else "Not Available",
                "FreeVirtualMemory": free_virtual.strip() if free_virtual else "Not Available",
                "Capacity": capacity.strip() if capacity else "Not Available",
                "MemoryType": memory_Type.strip() if memory_Type else "Not Available",
                "Speed": speed.strip() if speed else "Not Available",
            }
        }
    except Exception as e:
        return {"error": str(e)}
    
def get_storage_info():
    try:

        os_type = platform.system()  # Make sure this is set properly

        if os_type == "Windows":
            diskdrive_deviceid = run_command("wmic diskdrive get DeviceID | findstr /V DeviceID")
            diskdrive_model = run_command("wmic diskdrive get Model | findstr /V Model")
            diskdrive_size = run_command("wmic diskdrive get Size | findstr /V Size")
            diskdrive_interface = run_command("wmic diskdrive get InterfaceType | findstr /V InterfaceType")
            diskdrive_status = run_command("wmic diskdrive get Status | findstr /V Status")
            diskdrive_mediatype = run_command("wmic diskdrive get MediaType | findstr /V MediaType")
            partition_name = run_command(" wmic partition get Name | findstr /V Name")
            partition_index = run_command("wmic partition get Index | findstr /V Index")
            partition_boot = run_command("wmic partition get BootPartition | findstr /V BootPartition")
            partition_size = run_command("wmic partition get Size | findstr /V Size")
            logicaldisk_deviceid = run_command("wmic logicaldisk get DeviceID | findstr /V DeviceID")
            logicaldisk_filesys = run_command(" wmic logicaldisk get FileSystem | findstr /V FileSystem")
            logicaldisk_size = run_command("wmic logicaldisk get Size | findstr /V Size")
            logicaldisk_freespace = run_command("wmic logicaldisk get FreeSpace | findstr /V FreeSpace")
            logicaldisk_volserialno = run_command("wmic logicaldisk get VolumeSerialNumber | findstr /V VolumeSerialNumber")
        
        else:  # For Linux, using lsblk
            diskdrive_mediatype = run_command("lsblk -d -o name,rota")

        return {
            "Storage Info": {
                "Disk Drive Device ID" : diskdrive_deviceid.strip() if diskdrive_deviceid else "Not Available",
                "Disk Drive Model" : diskdrive_model.strip() if diskdrive_model else "Not Available",
                "Disk Drive Size" : diskdrive_size.strip() if diskdrive_size else "Not Available",
                "Disk Drive Interface" : diskdrive_interface.strip() if diskdrive_interface else "Not Available",
                "Disk Drive Status" : diskdrive_status.strip() if diskdrive_status else "Not Available",
                "Disk Drive Media Type" : diskdrive_mediatype.strip() if diskdrive_mediatype else "Not Available",
                "Partition Name" : partition_name.strip() if partition_name else "Not Available",
                "Partition Index" : partition_index.strip() if partition_index else "Not Available",
                "Partition Boot" : partition_boot.strip() if partition_boot else "Not Available",
                "Partition Size" : partition_size.strip() if partition_size else "Not Available",
                "Logical Disk Device ID" : logicaldisk_deviceid.strip() if logicaldisk_deviceid else "Not Available",
                "Logical Disk File System" : logicaldisk_filesys.strip() if logicaldisk_filesys else "Not Available",
                "Logical Disk Size" : logicaldisk_size.strip() if logicaldisk_size else "Not Available",
                "Logical Disk Free Space" : logicaldisk_freespace.strip() if logicaldisk_freespace else "Not Available",
                "Logical Disk Volume Serial Number" : logicaldisk_volserialno.strip() if logicaldisk_volserialno else "Not Available",
            }
        }
    except Exception as e:
        return {"error": str(e)}

def get_audio_info():
    try:
        os_type = platform.system()
        
        if os_type == "Windows":
            sound_card = run_command("wmic sounddev get Name | findstr /V Name")
            playback = run_command('wmic path Win32_PnPEntity where "Name like \'%Audio%\'" get Name | findstr /V Name')
            
            sound_card_list = sound_card.splitlines() if sound_card else []
            playback_list = playback.splitlines() if playback else []
        
        else:  # Linux Commands
            playback = run_command("aplay -l")
            playback_list = playback.splitlines() if playback else []
            sound_card_list = []

        # Clean up and remove empty lines
        sound_card_list = [s.strip() for s in sound_card_list if s.strip()]
        playback_list = [p.strip() for p in playback_list if p.strip()]

        return {
            "Audio Info": {
                "Sound Card": sound_card_list,  # Returning as a list
                "Playback": playback_list,  # Returning as a list
            },
        }
    except Exception as e:
        return {"error": str(e)}

def get_network_info():
    try:
        os_type = platform.system()
        
        if os_type == "Windows":
            internet_name = run_command(" wmic path Win32_NetworkAdapter where \"NetConnectionStatus=2\" get Name | findstr /V Name")
            internet_connectstatus = run_command(" wmic path Win32_NetworkAdapter where \"NetConnectionStatus=2\" get NetConnectionStatus | findstr /V NetConnectionStatus")
            networdadpt_name = run_command("wmic nic get Name | findstr /V Name")
            networkadpt_netenable = run_command("wmic nic get NetEnabled | findstr /V NetEnabled")
            networkadpt_macaddr = run_command("wmic nic get MACAddress | findstr /V MACAddress")
            networkadpt_speed = run_command("wmic nic get Speed | findstr /V Speed")
            networkadpt_adptype = run_command("wmic nic get AdapterType | findstr /V AdapterType")
            descrp = run_command("wmic path Win32_NetworkAdapterConfiguration get Description | findstr /V Description")
            ip_addr = run_command("wmic path Win32_NetworkAdapterConfiguration get IPAddress | findstr /V IPAddress")
            mac_addr = run_command("wmic path Win32_NetworkAdapterConfiguration get MACAddress | findstr /V MACAddress")
            ip_gateway = run_command("wmic path Win32_NetworkAdapterConfiguration get DefaultIPGateway | findstr /V DefaultIPGateway")
            dns_server = run_command("wmic path Win32_NetworkAdapterConfiguration get DNSServerSearchOrder | findstr /V DNSServerSearchOrder")
            dhcp_server = run_command("wmic path Win32_NetworkAdapterConfiguration get DHCPServer | findstr /V DHCPServer")
            wifi_name = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get Name | findstr /V Name")
            wifi_macaddr = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get MACAddress | findstr /V MACAddress")
            wifi_speed = run_command("wmic path Win32_NetworkAdapter where \"Name like '%Wi-Fi%'\" get Speed | findstr /V Speed")
            comp_name = run_command("wmic computersystem get Name | findstr /V Name")
            comp_workgrp = run_command("wmic computersystem get Workgroup | findstr /V Workgroup")

        else:  # Linux Commands
            ip_addr = run_command("ip addr show")
            
        return {
            "Network Info": {
                "Internet Name" : internet_name.strip() if internet_name else "Not Available",
                "Internet ConnectStatus" : internet_connectstatus.strip() if internet_connectstatus else "Not Available",
                "Network Adapter Name" : networdadpt_name.strip() if networdadpt_name else "Not Available",
                "Network Adapter NetEnable" : networkadpt_netenable.strip() if networkadpt_netenable else "Not Available",
                "Network Adapter MACAddress" : networkadpt_macaddr.strip() if networkadpt_macaddr else "Not Available",
                "Network Adapter Speed" : networkadpt_speed.strip() if networkadpt_speed else "Not Available",
                "Network Adapter AdpType" : networkadpt_adptype.strip() if networkadpt_adptype else "Not Available",
                "Description" : descrp.strip() if descrp else "Not Available",
                "IP Address" : ip_addr.strip() if ip_addr else "Not Available",
                "MAC Address" : mac_addr.strip() if mac_addr else "Not Available",
                "IP Gateway" : ip_gateway.strip() if ip_gateway else "Not Available",
                "DNS Server" : dns_server.strip() if dns_server else "Not Available",
                "DHCP Server" : dhcp_server.strip() if dhcp_server else "Not Available",
                "Wi-Fi Name" : wifi_name.strip() if wifi_name else "Not Available",
                "Wi-Fi MACAddress" : wifi_macaddr.strip() if wifi_macaddr else "Not Available",
                "Wi-Fi Speed" : wifi_speed.strip() if wifi_speed else "Not Available",
                "Computer Name" : comp_name.strip() if comp_name else "Not Available",
                "Computer Workgroup" : comp_workgrp.strip() if comp_workgrp else "Not Available",
            },
        }
    except Exception as e:
        return {"error": str(e)}

def get_peripherals_info():
    try:
        os_type = platform.system()

        if os_type == "Windows":
            keyb_name = run_command("wmic path Win32_Keyboard get Name")
            keyb_dscp = run_command("wmic path Win32_Keyboard get Description")
            keyb_deviceid = run_command("wmic path Win32_Keyboard get DeviceID")
            mouse_name = run_command("wmic path Win32_PointingDevice get Name")
            mouse_deviceid = run_command("wmic path Win32_PointingDevice get DeviceID")
            printer_name = run_command("wmic printer get Name")
            printer_port = run_command("wmic printer get PortName")
            printer_processor = run_command("wmic printer get PrintProcessor")
            printer_drivern = run_command("wmic printer get DriverName")

            # Convert outputs into lists for structured display
            keyboard_list = keyb_name.splitlines()[1:] if keyb_name else []
            keyboard_desc_list = keyb_dscp.splitlines()[1:] if keyb_dscp else []
            keyboard_id_list = keyb_deviceid.splitlines()[1:] if keyb_deviceid else []
            mouse_list = mouse_name.splitlines()[1:] if mouse_name else []
            mouse_id_list = mouse_deviceid.splitlines()[1:] if mouse_deviceid else []
            printer_list = printer_name.splitlines()[1:] if printer_name else []
            port_list = printer_port.splitlines()[1:] if printer_port else []
            processor_list = printer_processor.splitlines()[1:] if printer_processor else []
            driver_list = printer_drivern.splitlines()[1:] if printer_drivern else []

        else:  # Linux Commands
            keyboard_list = ["Not Available"]
            mouse_list = ["Not Available"]
            printer_list = run_command("lpstat -p").splitlines() if run_command("lpstat -p") else ["Not Available"]

        return {
            "Peripherals Info": {
                "Keyboard": keyboard_list,
                "Keyboard Description": keyboard_desc_list,
                "Keyboard DeviceID": keyboard_id_list,
                "Mouse": mouse_list,
                "Mouse DeviceID": mouse_id_list,
                "Printer": printer_list,
                "Port Name": port_list,
                "Print Processor": processor_list,
                "Driver Name": driver_list,
            },
        }
    except Exception as e:
        return {"error": str(e)}

def get_software():
    try:
        os_type = platform.system()
        
        if os_type == "Windows":
            name = run_command("wmic product get Name | findstr /V Name")
            software_list = name.splitlines() if name else []  # Split by new lines
        else:  # Linux
            name = run_command("apt list --installed")
            software_list = name.splitlines() if name else []

        # Clean and format the list
        software_list = [s.strip() for s in software_list if s.strip()]

        return {
            "Software Installed": {
                "Name": software_list,  # This is now a proper list
            },
        }
    except Exception as e:
        return {"error": str(e)}



# def index(request):
#     return render(request, 'index.html')

def summary(request):
    return render(request, 'summary.html')

def os_info(request):
    return render(request, 'os.html')

def cpu(request):
    return render(request, 'cpu.html')

def motherboard(request):
    return render(request, 'motherboard.html')

def gpu(request):
    return render(request, 'gpu.html')

def ram(request):
    return render(request, 'ram.html')

def storage(request):
    return render(request, 'storage.html')

def audio(request):
    return render(request, 'audio.html')

def network(request):
    return render(request, 'network.html')

def peripherals(request):
    return render(request, 'peripherals.html')

def software(request):
    return render(request, 'software.html')

def system_info(request):
    try:
        refresh = request.GET.get('refresh', 'false').lower() == 'true'
        
        # Check if cache exists and refresh is not requested
        if not refresh:
            cached_data = cache.get('system_info')
            if cached_data:
                return JsonResponse(cached_data)

        # Fetch new data
        data = get_os_info()
        data1 = get_cpu_info()
        data2 = get_summary()
        data3 = get_motherboard_info()
        data4 = get_gpu_info()
        data5 = get_ram_info()
        data6 = get_storage_info()
        data7 = get_audio_info()
        data8 = get_network_info()
        data9 = get_peripherals_info()
        data10 = get_software()
        combined_data = {**data, **data1, **data2, **data3, **data4, **data5, **data6, **data7, **data8, **data9, **data10}

        # Store in cache
        cache.set('system_info', combined_data, timeout=900)

        return JsonResponse(combined_data)

    except Exception as e:
        return JsonResponse({"error": str(e)})
