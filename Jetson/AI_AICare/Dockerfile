FROM nvcr.io/nvidia/l4t-base:r32.3.1

RUN apt-get update
RUN apt-get install -y python3-pip nano
RUN pip3 install -U pip
RUN apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
RUN pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast
RUN apt-get install -y python3-h5py
RUN pip3 install astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta
RUN pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu==1.15.0
RUN pip3 install flask tornado Pillow
RUN pip3 install keras --no-depend
RUN apt-get install -y python3-scipy p7zip-full

RUN apt-get install -y libsm6 libxext6 libxrender-dev

ARG DEBIAN_FRONTEND=noninteractive
RUN apt install -y python3-opencv
RUN pip3 install pynput
RUN pip3 install pyyaml
RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module
RUN apt-get install -y python-gst-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools

COPY ./FaceMaskDetection /home/smasoft/AI_AICare/FaceMaskDetection

EXPOSE 8001

# Set the working directory
WORKDIR /home/smasoft/AI_AICare/FaceMaskDetection

RUN ["chmod","+x","run.sh"]

ENTRYPOINT ["bash", "run.sh"]
