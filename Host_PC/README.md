# Thermal MaskAI Host PC Setup
![Overall Schematic Host PC](/Host_PC/Overall_Schematic_HostPC.png)

# Make sure you have setup your Jetson Device following the instructions outlined in the README under "Jetson" folder of this repository

# Step 1: (On Host PC): Install mvGenTL_Acquire x86_64

1. Install **"mvGenTL_Acquire-x86_64-2.37.1.exe"** from this [link](http://static.matrix-vision.com/mvIMPACT_Acquire/2.37.1/)

# Step 2: (On Host PC): Build and install python binding package

1. Install the [CCompiler](https://wiki.python.org/moin/WindowsCompilers#Which_Microsoft_Visual_C.2B-.2B-_compiler_to_use_with_a_specific_Python_version_.3F) corresponding to your python version (3.6.x ==> MSVC Build Tools 14.2)
2. go to **"C:\Program Files\MATRIX VISION\mvIMPACT Acquire\LanguageBindings\Python"** and run **"compileWrapperCode.bat"** as administrator

# Step 3: Setup all hardwares
1. Connect usb camera (optical) with host computer
2. Connect thermal camera (GigE interface) with host computer via ethernet cable (set this ethernet port to **DHCP**)
3. Connect Jetson device with host computer via ethernet cable (set this ethernet port to **static 192.168.99.10**)

![Cameras Setup](/media/Cameras_Setup.jpg)

# Step 4: (On Host PC): Execute Image & Thermal acquisition python code!
1. Make sure your Jetson device is up and running and execute **"python maskai.py"** using command line interface

# Step 5: (On Host PC): Start viewing live detection!
1. open any browser and go to: **"127.0.0.1:8432/video_feed"** to view live facial mask detection along with human forehead temperature detection

![Detection In Action](/media/Detection_In_Action_2.jpg)

# IMPORTANT: make sure your thermal camera is set to output "uint16" thermal data array