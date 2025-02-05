# # # from django.shortcuts import render
# # # import platform
# # # from django.http import JsonResponse
# # # from django.http import HttpResponse
# # # import subprocess
# # # def index(request):
# # #     return render(request, 'index.html')
# # # def os(request):
# # #     os_name = platform.system()  # e.g., 'Windows', 'Linux', 'Darwin' (MacOS)
# # #     os_version = platform.version()  # Detailed version info
# # #     os_release = platform.release()  # Release name
# # #     return JsonResponse({
# # #         'os_name': os_name,
# # #         'os_version' : os_version,
# # #         'os_release' : os_release,
# # #     })
# # # def runcmd(command):
# # #     try:
# # #         # Run the command
# # #         result = subprocess.run(command, capture_output=True, text=True, shell=True)
# # #         if result.stdout:
# # #             return result.stdout.strip()
# # #         elif result.stderr:
# # #             return f"Error: {result.stderr.strip()}"
# # #         else:
# # #             return "No output"
# # #     except Exception as e:
# # #         return f"Exception occurred: {str(e)}"
# # # def system_info(request): 
# # #     # Commands to execute
# # #     commands = {
# # #         "OS Name": "wmic os get Caption",
# # #         "OS Version" : "wmic os get Version",
# # #         "Build Number": "wmic os get BuildNumber",
# # #         "Kernel Version": "wmic os get Version",
# # #         "Processor Usage": "wmic cpu get LoadPercentage",
# # #         "Memory Usage": "wmic OS get FreePhysicalMemory,\n TotalVisibleMemorySize",
# # #         "Swap Memory Usage": "wmic OS get FreeVirtualMemory,TotalVirtualMemorySize",
# # #         "IP Address": "ipconfig",
# # #     }
# # #     # Execute commands and collect results
# # #     results = {}
# # #     for description, command in commands.items():
# # #         results[description] = runcmd(command)
# # #     # Return results as a JSON response
# # #     return JsonResponse(results)





# # from django.shortcuts import render
# # from django.http import JsonResponse
# # import subprocess
# # import re
# # def run_command(command):
# #     try:
# #         return subprocess.check_output(command, shell=True, text=True)
# #     except subprocess.CalledProcessError as e:
# #         return str(e)  
# # def index(request):
# #     # You can render the home page template here or simply return a response
# #     return render(request, 'index.html')
# # def process_command_output(command, filters):
# #     output = run_command(command).splitlines()
# #     info = {}
# #     capturing = False
# #     for line in output:
# #         line = line.strip()
# #         for key, filter_value in filters.items():
# #             if key in line:
# #                 info[key] = line.split(":")[-1].strip()
# #     return info
# # def system_info(request):
# #     try:
# #         # Define the commands and the filters
# #         # commands = {
# #         #     "OS Info": ("systeminfo", {
# #         #         "OS Name": "OS Name",
# #         #         "OS Version": "OS Version",
# #         #         "System Model": "System Model",
# #         #     },"ipconfig",{
# #         #         "IPv4 Address": "IPv4 Address",
# #         #         "Subnet Mask": "Subnet Mask",
# #         #     }),
# #         #     "CPU Info": ("Get-WmiObject -Class Win32_Processor | Select-Object Name", {
# #         #         "CPU Name": "CPU Name",
# #         #     },"Get-WmiObject -Class Win32_Processor | Select-Object Architecture",{
# #         #         "CPU Architecture": "CPU Architecture",
# #         #     })
# #         # }
# #         commands = {
# #             "OS Info": {
# #                 "Command": "systeminfo",
# #                 "Fields": {
# #                     "OS Name": "OS Name",
# #                     "OS Version": "OS Version",
# #                     "System Model": "System Model",
# #                 },
# #                 "Additional Command": "ipconfig",
# #                 "Additional Fields": {
# #                     "IPv4 Address": "IPv4 Address",
# #                     "Subnet Mask": "Subnet Mask",
# #                 },
# #             },
# #             "CPU Info": {
# #                 "Command": "Get-WmiObject -Class Win32_Processor | Select-Object Name",
# #                 "Fields": {
# #                     "CPU Name": "CPU Name",
# #                 },
# #                 "Additional Command": "Get-WmiObject -Class Win32_Processor | Select-Object Architecture",
# #                 "Additional Fields": {
# #                     "CPU Architecture": "CPU Architecture",
# #                 },
# #             },
# #         }
# #         results = {}
# #         # Loop over each command and process its output
# #         for description, (command, filters) in commands.items():
# #             results[description] = process_command_output(command, filters)
# #         return JsonResponse(results)
# #     except Exception as e:
# #         return JsonResponse({"error": str(e)})
# # def system_info_ui(request):
# #     return render(request, 'index.html')
# # from django.http import JsonResponse
# # from django.shortcuts import render
# # import subprocess
# # # Helper function to run terminal commands
# # def run_command(command):
# #     try:
# #         result = subprocess.check_output(command, shell=True, text=True).strip()
# #         return result
# #     except subprocess.CalledProcessError as e:
# #         return f"Error: {e}"
# # def get_system_info():
# #     try:
# #         os_name = run_command("systeminfo")  # Command to get OS name
# #         ip_address = run_command("ipconfig")  # Command to get IP address
# #         cpu_name = run_command("wmic cpu get name")
# #         cpu_architecture = run_command("wmic cpu get architecture")
# #         return {
# #             "OS Info": {
# #                 "OS Name": os_name,
# #                 "OS Version": os_name,  # Placeholder, replace with actual command if needed
# #                 "OS Architecture": os_name,  # Placeholder, replace with actual command if needed
# #                 "IPv4 Address": ip_address,
# #                 "Subnet Mask": ip_address,  # Placeholder, replace with actual command if needed
# #             },
# #             "CPU Info": {
# #                 "CPU Name": cpu_name,  # Example data
# #                 "CPU Architecture": cpu_architecture,  # Example data
# #             },
# #         }
# #     except Exception as e:
# #         return {"error": str(e)}
# # def index(request):
# #     return render(request, 'index.html')
# # def system_info(request):
# #     try:
# #         data = get_system_info()
# #         return JsonResponse(data)
# #     except Exception as e:
# #         return JsonResponse({"error": str(e)})




# from django.http import JsonResponse
# from django.shortcuts import render
# import subprocess
# # Helper function to run terminal commands and extract relevant information
# def run_command(command, parse_output=False):
#     try:
#         result = subprocess.check_output(command, shell=True, text=True).strip()
#         if parse_output:
#             # For specific commands that need parsing, return only the required information
#             result_lines = result.splitlines()
#             # Extracting the first line if needed, for specific commands like "systeminfo" and "ipconfig"
#             return result_lines[0] if result_lines else ""
#         return result
#     except subprocess.CalledProcessError as e:
#         return f"Error: {e}"
# def get_system_info():
#     try:
#         # Extracting only the relevant info from each command
#         os_name = run_command("systeminfo | findstr /B /C:\"OS Name\"", parse_output=True)
#         os_version = run_command("systeminfo | findstr /B /C:\"OS Version\"", parse_output=True)
#         os_architecture = run_command("systeminfo | findstr /B /C:\"System Type\"", parse_output=True)
#         ip_address = run_command("ipconfig | findstr /R /C:\"Wireless LAN adapter\" /C:\"IPv4\"", parse_output=True)
#         subnet_mask = run_command("ipconfig | findstr /R /C:\"Subnet\"", parse_output=True)
#         # Extracting the CPU information (unchanged)
#         cpu_name = run_command("wmic cpu get name")
#         cpu_architecture = run_command("wmic cpu get architecture")
#         cpu_socketdesignation = run_command("wmic cpu get SocketDesignation")
#         cpu_nocores = run_command(" wmic cpu get NumberOfCores")
#         cpu_logicalproc = run_command("wmic cpu get NumberOfLogicalProcessors")
#         cpu_frequency = run_command("wmic cpu get CurrentClockSpeed")
#         return {
#             "OS Info": {
#                 "OS Name": os_name.split(":")[1].strip() if os_name else "Not Available",
#                 "OS Version": os_version.split(":")[1].strip() if os_version else "Not Available",
#                 "OS Architecture": os_architecture.split(":")[1].strip() if os_architecture else "Not Available",
#                 "IPv4 Address": ip_address.split(":")[1].strip() if ip_address else "Not Available",
#                 "Subnet Mask": subnet_mask.split(":")[1].strip() if ip_address else "Not Available",
#             },
#             "CPU Info": {
#                 "CPU Name": cpu_name.strip(),
#                 "CPU Architecture": cpu_architecture.strip(),
#                 "Socket Designation": cpu_socketdesignation.strip(),
#                 "Number Of Cores" : cpu_nocores.strip(),
#                 "Number Of Logical Processors": cpu_logicalproc.strip(),
#                 "Frequency" : cpu_frequency.strip(),
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}
# def index(request):
#     return render(request, 'index.html')
# def system_info(request):
#     try:
#         data = get_system_info()
#         return JsonResponse(data)
#     except Exception as e:
#         return JsonResponse({"error": str(e)})








# from django.http import JsonResponse
# from django.shortcuts import render
# import subprocess
# import re
# import wmi
# # Helper function to run terminal commands
# def run_command(command):
#     try:
#         result = subprocess.check_output(command, shell=True, text=True).strip()
#         return result
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
# def get_cpu_temperature():
#     try:
#         w = wmi.WMI(namespace="root\wmi")
#         temp_sensors = w.MSAcpi_ThermalZoneTemperature()
#         if temp_sensors:
#             temperature = (temp_sensors[0].CurrentTemperature - 2732) / 10  # Convert from deciKelvin to Celsius
#             return f"{temperature}°C"
#         return "Temperature data not available"
#     except Exception as e:
#         return f"Error: {str(e)}"
# def get_system_info():
#     try:
#         os_name = run_command("wmic os get Caption | findstr /V Caption")
#         os_version = run_command("wmic os get Version | findstr /V Version")
#         os_architecture = run_command("wmic os get OSArchitecture | findstr /V OSArchitecture")
#         wifi_ipv4_address = get_wifi_ipv4()
#         cpu_name = run_command("wmic cpu get name | findstr /V Name")
#         cpu_architecture = run_command("wmic cpu get architecture | findstr /V Architecture")
#         cpu_socketdesignation = run_command("wmic cpu get SocketDesignation")
#         cpu_nocores = run_command(" wmic cpu get NumberOfCores")
#         cpu_logicalproc = run_command("wmic cpu get NumberOfLogicalProcessors")
#         cpu_frequency = run_command("wmic cpu get CurrentClockSpeed")
#         cpu_loadper = run_command("wmic cpu get LoadPercentage")
#         cpu_temp = get_cpu_temperature()
#         # cpu_temp = run_command('powershell -Command "((Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace \'root/wmi\').CurrentTemperature - 2732) / 10"')
#         cpu_volt = run_command(" wmic cpu get CurrentVoltage")
#         cpu_descrip = run_command("wmic cpu get Description")
#         return {
#             "OS Info": {
#                 "OS Name": os_name.strip() if os_name else "Not Available",
#                 "OS Version": os_version.strip() if os_version else "Not Available",
#                 "OS Architecture": os_architecture.strip() if os_architecture else "Not Available",
#                 "Wi-Fi IPv4 Address": wifi_ipv4_address,
#             },
#             "CPU Info": {
#                 "CPU Name": cpu_name.strip() if cpu_name else "Not Available",
#                 "CPU Architecture": cpu_architecture.strip() if cpu_architecture else "Not Available",
#                 "Socket Designation": cpu_socketdesignation.strip(),
#                 "Number Of Cores" : cpu_nocores.strip(),
#                 "Number Of Logical Processors": cpu_logicalproc.strip(),
#                 "Frequency" : cpu_frequency.strip(),
#                 "Load Percentage" : cpu_loadper.strip(),
#                 "CPU Temperature" : cpu_temp.strip(),
#                 "CPU Voltage" : cpu_volt.strip(),
#                 "CPU Description" : cpu_descrip.strip(),
#             },
#         }
#     except Exception as e:
#         return {"error": str(e)}
# def index(request):
#     return render(request, 'index.html')
# def system_info(request):
#     try:
#         data = get_system_info()
#         return JsonResponse(data)
#     except Exception as e:
#         return JsonResponse({"error": str(e)})







from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
import platform
import subprocess
import re
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            serial_no = form.cleaned_data.get('serial_no')
            password = form.cleaned_data.get('password')
            # TODO: Implement authentication logic here
            messages.error(request, 'Invalid credentials')
            return redirect('summary')
            # return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        return result
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
            os_version = run_command("lsb_release -r | awk -F'\t' '{print $2}'")
            os_architecture = run_command("uname -m")
            os_manufacturer = run_command("cat /sys/class/dmi/id/sys_vendor")
            os_serialno = run_command("cat /sys/class/dmi/id/product_serial")
            os_installdate = "Not Available"

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

# def index(request):
#     return render(request, 'index.html')

def summary(request):
    return render(request, 'summary.html')

def os(request):
    return render(request, 'os.html')

def cpu(request):
    return render(request, 'cpu.html')

# def system_info(request):
#     try:
#         data = get_os_info()
#         data1 = get_cpu_info()
#         data2 = get_summary()
#         combine_data = {**data, **data1, **data2}
#         return JsonResponse(combine_data)
#     except Exception as e:
#         return JsonResponse({"error": str(e)})

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
        combined_data = {**data, **data1, **data2}

        # Store in cache
        cache.set('system_info', combined_data, timeout=900)

        return JsonResponse(combined_data)

    except Exception as e:
        return JsonResponse({"error": str(e)})

