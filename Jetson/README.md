# MaskAI_On_Jetson_Setup
# Step 1: We will need to first setup an Azure Container Registry for storing our FaceMask_Detection docker container image
# Step 2: Then we will create the docker FaceMask_Detection docker container image and push it onto the Azure Container Registry created
# Step 3: Create an Azure IoTHub, IoTEdge Device and IoTEdge Module
# Step 4: Install Azure IoTEdge Runtime and link our actual Jetson Device (acting as an edge device) with Azure's IoTEdge Device on cloud 

Step 1 (On any computer with network capability):
1. This link outlines how to create an Azure ResourceGroup and Azure Container Registry (ACR) using CLI: https://docs.microsoft.com/zh-tw/azure/container-registry/container-registry-get-started-azure-cli (you are fine once you can log into your ACR, you do not have to do everything in the tutorial)
2. Once ACR is created, go to your ACR on portal.azure.com and copy the {Login Server}, {Username} and {Password}; you will need these later

Step 2 (On Jetson):
1. Flash your Nvidia Jetson device with JetPack 4.2.2 (follow the steps in this link): https://developer.nvidia.com/jetpack-422-archive
2. Open up ubuntu Terminal on our Jetson Device
3. sudo nano /etc/docker/daemon.json
4. add "default-runtime": "nvidia"
5. sudo systemctl restart docker
6. Copy repository's entire "AI_AICare" folder into /home/{$user}/
7. cd /home/{$user}/AI_AICare
8. sudo docker build -t {azure_repository_name}/{image_name_of_your_choice} .
9. sudo docker push {azure_repository_name}/{image_name_of_your_choice}



