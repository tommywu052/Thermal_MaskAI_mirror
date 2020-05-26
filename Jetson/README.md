# MaskAI_On_Jetson_Setup
# Step 1 (PC/Jetson): Create an Azure ResourceGroup and Container Registry
1. This [link](https://docs.microsoft.com/zh-tw/azure/container-registry/container-registry-get-started-azure-cli) outlines how to create an **Azure ResourceGroup** and **Azure Container Registry (ACR)** using CLI (you are fine once you can log into your ACR, you do not have to do everything in the tutorial)
2. Once **ACR** is created, go to your **ACR ==> Access Keys (tab)** on [Azure Portal](https://portal.azure.com), copy the **{Login Server}**, **{Username}** and **{Password}**; you will need these later
3. Also, take note of your **{resource group name}** for the ResourceGroup you created earlier

# Step 2 (Jetson): Create docker container image
1. Flash your Nvidia Jetson device with [JetPack 4.2.2](https://developer.nvidia.com/jetpack-422-archive) (follow the steps in this link)
2. Make sure your Jetson Device is connected to the internet (cable preferably, WiFi not advised), and on the upper right set powermode to 0: MAXN
3. Open up ubuntu Terminal on our Jetson Device
4. **sudo nano /etc/docker/daemon.json**
5. add **"default-runtime": "nvidia"**
6. **sudo systemctl restart docker**
7. Copy repository's entire "AI_AICare" folder into **/home/{$user}/**
8. **cd /home/{$user}/AI_AICare**
9. **sudo docker login {Login Server}**, and input your **{Username}** and **{Password}** when prompted
10. **sudo docker build -t {Login Server}/{image_name_of_your_choice} .**
11. **sudo docker push {Login Server}/{image_name_of_your_choice}**

# Step 3: (PC/Jetson): Create an Azure IoTHub, IoTEdge Device and IoTEdge Module
1. Create an [Azure IoTHub](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-create-using-cli), and remember your **{hub_name}**
2. Create an EdgeDevice under the IoTHub using Azure CLI with this command: **az iot hub device-identity create --hub-name **{hub_name}** --device-id **myEdgeDevice** --edge-enabled**
3. Retrieve the **{CONNECTION_STRING}** for your EdgeDevice (this is very important) with this command: **az iot hub device-identity show-connection-string --device-id **myEdgeDevice** --hub-name **{hub_name}****
4. Next, sign in to your [Azure Portal](https://portal.azure.com) and navigate to your IoTHub
5. On the left pane, select "IoT Edge" from the menu
6. Click on your Device ID (i.e. myEdgeDevice)
7. On the upper bar, select "Set Modules"
8. In the "Container Registry Settings" section of the page, provide your **{Login Server}** as the ADDRESS, **{Username}** as NAME and USER NAME, and **{Password}** as PASSWORD
9. In the IoT Edge Modules section of the page, select Add
10. Select "IoT Edge Module" from the drop-down menu, and provide your own module name, and in the "Image URI" section ENTER **{Login Server}/{image_name_of_your_choice}** (note that this is the container image that you "docker pushed" earlier)
11. Once that's done, select the "Container Create Options" tab and copy & paste these:
```json 
{
    "HostConfig": {
        "PortBindings": {
            "8001/tcp": [
                {
                    "HostPort": "8001"
                }
            ]
        }
    }
}
```
12.  Finally, press the "Update" button, then "Review + create" button and then press "Create" after; the Edge module should be up and running

# Step 4: (Jetson): Install Azure IoTEdge Runtime
1. Back on Jetson Device, open up ubuntu Terminal (make sure you have "curl" installed with **sudo apt-get install curl**)
2. **curl https://packages.microsoft.com/config/ubuntu/18.04/multiarch/prod.list > ./microsoft-prod.list**
3. **sudo cp ./microsoft-prod.list /etc/apt/sources.list.d/**
4. **curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg**
5. **sudo cp ./microsoft.gpg /etc/apt/trusted.gpg.d/**
6. **sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak**
7. **sudo mkdir /var/lib/dpkg/info**
8. **sudo apt update**
9. **sudo apt install -f moby-engine**
10. **sudo apt install -f moby-cli**
11. **sudo mv /var/lib/dpkg/info/*** **/var/lib/dpkg/info.bak**
12. **ls -a /var/lib/dpkg/info**
13. **sudo rm -rf /var/lib/dpkg/info**
14. **sudo mv /var/lib/dpkg/info.bak /var/lib/dpkg/info**
15. **sudo apt-get update**
16. **sudo apt-get install iotedge**
17. **sudo nano /etc/iotedge/config.yaml**
18. search for and enter your previously retrieved **{CONNECTION_STRING}** into the quotations of this line: **device_connection_string: "*ADD DEVICE CONNECTION STRING HERE*"**
19. press ctrl+x, shift+y, ENTER
20. **sudo systemctl restart iotedge**
21. **sudo reboot**
22. After Jetson Device has rebooted, wait for around 15min or so for iotedge, along with the modules running your container image to startup. You can check if everything is up and running by typing "sudo iotedge list"
23. Once everything is up and running (you should see 3 modules running, namely edgeAgent, edgeHub and {your module name}), go to the upper right corner of ubuntu desktop and set ipv4 address of your Jetson Device to "Manual" with IP as: **"192.168.99.95"**, and netmask as: **"24" or "255.255.255.0"**
24. reboot again and now the Face Mask Detection AI Server on your Jetson Device will run automatically



