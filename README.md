# Physical Interfaces / Creative Robotics 
winter term 2024/2025

Augsburg Technical University of Applied Sciences, Prof. Andreas Muxel
 
# Universal Robots Simulation (Windows only)
* Download and install URSim here (account necessary, but it's free): https://www.universal-robots.com/download/software-e-series/simulator-non-linux/offline-simulator-e-series-ur-sim-for-non-linux-5126-lts/
* Unzip it to the folder of your choice

# Virtual Box (Windows only)
* Download and install VirtualBox here: https://www.virtualbox.org/wiki/Downloads
* Start VirtualBox and press 'New'
* Define name (your choice), Type: Linux, Version: Ubuntu (64-bit) - press ‘Next’
* Select Memory size of 768 MB and press 'Next'
* Select ‘Use an existing hard drive file’ and define the path to the folder where the zipped file was unpacked, select the file URSim_VIRTUAL-5.12.6.1102099.vmdk and press ‘Open’. Press ‘Next’. Press ‘Finish’.
* Go to ‘Settings’ - ‘Network’ - ‘Adapter 1’ and pick Bridged Adapter for ‘Attached to’ and select your Ethernet Connection for ‘Name’. Press ‘Ok’.
* Go to ‘Settings’ - ‘Display’ - ‘Screen’ and change Video memory to 60 MB and select VBoxVGA for the Graphics Controller. Press ‘Ok’.
* Press 'Start' to start the virtual machine
* If an error saying 'Hardware acceleration is not available' is shown then it may be required to reboot the Windows computer into BIOS setup and enable hardware access to * Virtual Machines and then restart Windows, VirtualBox and the virtual machine.
* Start the Virtual Machine
* Open "URSim UR5"
* Confirm Safety Configuration
* Select main menu top right "Settings"
* Navigate to "System"
* Check if "Network" is set to DHCP and if a network is connected (IP address, ...)
* Navigate to "Remote Control" and press button "Enable"
* Press EXIT (bottom left) 
* Press icon touchscreen (top right) and switch from "Local" to "Remote Control"
* Press "Power off" (bottom left) and switch on Robot witt Button "ON" and in a next step "START"
* To get the IP address of the robot select "About" in the burger menu (top right)

# Anaconda
* Download and install Anaconda here: https://www.anaconda.com/
* Once Anaconda is installed, open it, create a new environment and call it RTDE_OSC (make sure you are using a python version that is supported by the ur-rtde package here: https://pypi.org/project/ur-rtde/ -> 3.11 should work for Win64)
* video tutorial Prof. Michael Kipp: https://www.youtube.com/watch?v=sDKVHmPsEEY&t=29s
* start environment using the play button "Open Terminal"

# Visual Studio Code & OSC Interface
* Launch VS Code from Anaconda with RTDE_OSC selected in the top of the Home tab
* Type the following commands in the Terminal of VSCode:
    * pip install ur_rtde
    * pip install python-osc
* Find scripts to read and write data to robot via OSC (Open Sound Control) in subfolder of folder ["/Python"](https://github.com/HybridThingsLab/course-creative-robotics/tree/main/Python) of this repository
* Add folders to your workspace with "File/Add Folder to Workspace"
* Save workspace
* View Folder in "Explorer" (icon documents left)
* In the "Python/RTDE_OSC_read" folder in VSCode navigate to -> src\config.json and change the “ip” to the IP Address from URSim (burger menue top right "About")
* In the "Python/RTDE_OSC_write" folder in VSCode navigate to -> src\RobotController.py and change the “ip” to your IP Address from URSim
* Open two terminal windows in VSCode side-by-side
* In one terminal window change the directory to RTDE_OSC_read\src by typing "cd " and drag and drop "src" folder to terminal
* Run the script by typing "python main.py"
* In the other terminal window change the directory to RTDE_OSC_write\src by typing "cd " and drag and drop "src" folder to terminal
* Run the script by typing "python main.py --driverobot"
* you should get an message "INFO:root:connected!"
* open one example provided in the repository (p.ex. "TouchDesigner/02_RobotController/robotController.toe")
* To stop a python script press "ctrl+c" in the terminal
* To restart use UP or DOWN key to recall last prompts and press RETURN