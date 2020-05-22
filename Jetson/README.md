# MaskAI_On_Jetson_Setup

Steps:
1. Flash your Nvidia Jetson device with JetPack 4.2.2 (follows the steps in this link): https://developer.nvidia.com/jetpack-422-archive
2. Open up terminal and modify docker's daemon.json:
   sudo nano /etc/docker/daemon.json
   and make sure your daemon.json looks like:
   {
       "default-runtime": "nvidia",
       "runtimes": {
           "path": "nvidia-container-runtime",
           "runtimeArgs": []
       }
   }



