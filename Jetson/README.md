# MaskAI_On_Jetson_Setup
# Step 1 (On any computer with network capability): Create an Azure ResourceGroup and Container Registry for storing our FaceMask_Detection docker container image
1. This link outlines how to create an Azure ResourceGroup and Azure Container Registry (ACR) using CLI: https://docs.microsoft.com/zh-tw/azure/container-registry/container-registry-get-started-azure-cli (you are fine once you can log into your ACR, you do not have to do everything in the tutorial)
2. Once ACR is created, go to your ACR ==> Access Keys (tab) on portal.azure.com and copy the {Login Server}, {Username} and {Password}; you will need these later
3. Also, take note of your {resource group name} for the ResourceGroup you created earlier

# Step 2 (On Jetson): Then we will create the docker FaceMask_Detection docker container image and push it onto the Azure Container Registry created
1. Flash your Nvidia Jetson device with JetPack 4.2.2 (follow the steps in this link): https://developer.nvidia.com/jetpack-422-archive
2. Make sure your Jetson Device is connected to the internet (cable preferably, WiFi not advised)
3. Open up ubuntu Terminal on our Jetson Device
4. sudo nano /etc/docker/daemon.json
5. add "default-runtime": "nvidia"
6. sudo systemctl restart docker
7. Copy repository's entire "AI_AICare" folder into /home/{$user}/
8. cd /home/{$user}/AI_AICare
9. sudo docker login {Login Server}, and input your {Username} and {Password} when prompted
10. sudo docker build -t {Login Server}/{image_name_of_your_choice} .
11. sudo docker push {Login Server}/{image_name_of_your_choice}

# Step 3: Create an Azure IoTHub, IoTEdge Device and IoTEdge Module (On any computer with network capability, using Azure CLI)
1. Create an Azure IoTHub: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-create-using-cli, and remember your {hub_name}
2. Create an EdgeDevice under the IoTHub using Azure CLI with this command: az iot hub device-identity create --hub-name {hub_name} --device-id myEdgeDevice --edge-enabled
3. Retrieve the {CONNECTION_STRING} for your EdgeDevice (this is very important) with this command: az iot hub device-identity show-connection-string --device-id myEdgeDevice --hub-name {hub_name}
4. 

# Step 4: Install Azure IoTEdge Runtime (On Jetson) 



