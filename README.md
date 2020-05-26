# Thermal FaceMask Detection utilizing:
# Nvida Jetson & Azure IoTEdge
![Overall Schematic](/Overall_Schematic.png)

Everything in this repository will help you setup a thermal-mask-detection system using the hardwares below

# Hardware Requirements:
1. Nvidia Jetson Series (Xavier, Nano, TX2 ONLY)
2. A Host PC (Windows preferably, with 2 ethernet ports, **NO GPU needed**)
3. A Thermal Camera (FLIR or any other running on GigE interface)
4. An Optical Camera (USB webcam, or any other USB camera)
5. 2*Ethernet Cables

# Software Requirements:
1. An Azure account and can sign in onto [Azure Portal](https://portal.azure.com)
2. Installed python==3.6.x, opencv, flask on HostPC

# Step 1: Follow the instructions outlined in README of the "Jetson" folder to setup your Jetson Device first
# Step 2: Follow the instructions outlined in README of the "Host_PC" folder to setup your HostPC to finalize the solution

