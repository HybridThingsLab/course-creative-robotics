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
* Open the URSim UR5 program