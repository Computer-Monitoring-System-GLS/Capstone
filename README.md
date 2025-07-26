Computer Monitoring Tool (CMT) 


Overview:
The Computer Monitoring Tool (CMT) is a web-based application designed to monitor multiple devices within a network in real-time. Its primary goal is to provide centralized visibility and control over connected devices, especially for system administrators or IT teams.


Core Features:

1.	Device Monitoring (Client-Server Architecture)
    •	Server monitors multiple client machines over the same network.
    •	Clients send system information (CPU, RAM, storage, etc.) to the server via SSH.
2.	Real-Time Data Updates
    •	Displays live system statistics.
3.	Authentication
    •	Users must log in to access the system.
    •	Clients can view only their own system data.
    •	Server admin can view all connected devices.
4.	System Summary Dashboard
    •	Server dashboard lists all connected clients.
    •	Click on a device to view detailed system information.
    •	Sidebar with sections: CPU, Memory, Disk, Network, Motherboard, etc.
5.	Responsive Design
    •	Web UI designed for both desktop.


Technology Stack:

Layer	            Tools Used
Frontend	        HTML, CSS, JavaScript (template), Bootstrap
Backend	            Python, Django
Remote Access	    SSH (paramiko or subprocess)
Network Scan	    Nmap (for device discovery)
UI/UX Design	    Figma (used during prototyping)


Cybersecurity Considerations:

•	Authentication & Authorization for server and clients.
•	SSH Encryption for secure data transfer from client to server.
•	Restricted Access: Clients cannot access other devices' data.
•   Nmap Scanning: Used for device discovery; access is limited to admin and results are secured.


Use Cases:

•	College Labs: Track hardware/software status of all lab systems.
•	Small Businesses: Central IT monitoring from one dashboard.
•	Cybersecurity & Incident Response: Quickly detect performance anomalies or unauthorized devices.


How to Run CMT Project: 

1. In VS Code
Step 1: Open the Project in VS Code
•	Launch Visual Studio Code.
•	Go to File → Open Folder and select the main CMT project folder.

Step 2: Open the Terminal
•	In VS Code, open the terminal:
•	Go to Terminal → New Terminal

Step 3: Activate the Virtual Environment
In the terminal, run:
cd CMT        # Go to project folder
cd myvenv     # Enter virtual environment folder
cd Scripts    # Go into Scripts (Windows)
./activate    # Activate the virtual environment
cd ../..      # Go back to root project folder
You should now see (myvenv) at the start of your terminal line.

Step 4:
python manage.py runserver http://<server-ip>:8000/

2. For Admins
Step 1: Login to CMT
• Open the CMT web interface in your browser.
• Enter your admin credentials to log in.

Step 2: View Connected Devices
• Once logged in, navigate to the dashboard.
• Click on the PC icon to view all discovered IP addresses of devices connected to the network.

Step 3: Connect to a Device
• Click on any listed IP address.
• A prompt will appear asking for the SSH username and password of the selected device.
• Enter the credentials to proceed.

Step 4: Start Monitoring
• After successful authentication, the system will:
    • Establish a secure SSH connection.
    • Automatically fetch and display hardware/software data of the selected device.
• You can now monitor the system in real-time from the dashboard.


Dependencies: 

On both Server and Client machines:
•	Python 3.x
•	Django>=4.0
•	channels>=4.0
•	daphne>=4.0
•	paramiko>=3.0     # For SSH communication
•	python-nmap       # To run nmap scans from Python
•	psutil            # For system information (CPU, memory, etc.)
•	Pip
•	Django
•	Django Channels (channels)
•	Nmap (nmap)
•	Paramiko (paramiko) or SSH installed
