# MaskAI_On_Jetson_Setup
# Step 1: We will need to first setup an Azure Container Registry for storing our FaceMask_Detection docker container image
# Step 2: Then we will create the docker FaceMask_Detection docker container image and push it onto the Azure Container Registry created
# Step 3: Create an Azure IoTHub, IoTEdge Device and IoTEdge Module
# Step 4: Install Azure IoTEdge Runtime and link our actual Jetson Device (acting as an edge device) with Azure's IoTEdge Device on cloud 

Step 2:
1. Flash your Nvidia Jetson device with JetPack 4.2.2 (follow the steps in this link): https://developer.nvidia.com/jetpack-422-archive
2. Open up ubuntu Terminal
3. sudo nano /etc/docker/daemon.json
4. make sure your daemon.json looks like (press ctrl+x ==> shift+y ==> ENTER after modification):
{
    "default-runtime": "nvidia",
    "runtimes": {
        "path": "nvidia-container-runtime",
        "runtimeArgs": []
    }
}
5. sudo systemctl restart docker
6. Copy repository's entire "AI_AICare" folder into /home/{$user}/
7. cd /home/{$user}/AI_AICare
8. sudo docker build -t {azure_repository_name}/{image_name_of_your_choice} .
9. sudo docker push {azure_repository_name}/{image_name_of_your_choice}



