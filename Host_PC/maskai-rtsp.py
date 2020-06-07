#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import cv2, base64
import numpy as np
import requests
import json
import queue, threading
from flask import jsonify, Flask, render_template, Response
import time
import platform
import string, sys, os
# import all the stuff from mvIMPACT Acquire into the current scope
from mvIMPACT import acquire
# import all the mvIMPACT Acquire related helper function such as 'conditionalSetProperty' into the current scope
# If you want to use this module in your code feel free to do so but make sure the 'Common' folder resides in a sub-folder of your project then
from mvIMPACT.Common import exampleHelper
import ctypes
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():

    ########################################################
    ## Set up thermal camera acquisition using mvIMPACT
    ########################################################
    """ devMgr = acquire.DeviceManager()
    pDev = devMgr[0]
    if pDev == None:
        exampleHelper.requestENTERFromUser()
        sys.exit(-1)
    pDev.open()

    fi = acquire.FunctionInterface(pDev)
    statistics = acquire.Statistics(pDev)
    
    while fi.imageRequestSingle() == acquire.DMR_NO_ERROR:
        print("Buffer queued")
    pPreviousRequest = None
    
    exampleHelper.manuallyStartAcquisitionIfNeeded(pDev, fi) """

    #######################################
    ##Bufferless VideoCapture
    #######################################
    class VideoCapture:
        def __init__(self, name):
            self.cap = cv2.VideoCapture(name)
            self.q = queue.Queue()
            t = threading.Thread(target=self._reader)
            t.daemon = True
            t.start()
        # read frames as soon as they are available, keeping only most recent one
        def _reader(self):
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                if not self.q.empty():
                    try:
                        self.q.get_nowait()   # discard previous (unprocessed) frame
                    except queue.Empty:
                        pass
                self.q.put(frame)
        def read(self):
            return self.q.get()
        def releases(self):
            self.cap.release()

    class ipcamCapture:
        def __init__(self, URL):
            self.Frame = []
            self.status = False
            self.isstop = False
            
        # Connect to IP Camera for RTSP streaming
            self.capture = cv2.VideoCapture(URL)

        def start(self):
        # Push read program into thread，daemon=True means it will closed with the main program。
            print('ipcam started!')
            threading.Thread(target=self.queryframe, daemon=True, args=()).start()

        def stop(self):
        # close the loop
            self.isstop = True
            print('ipcam stopped!')
    
        def getframe(self):
        # get the latest frame when needed (paried with cv2.waitKey(your ms) )
            return self.Frame
            
        def queryframe(self):
            while (not self.isstop):
                self.status, self.Frame = self.capture.read()
            
            self.capture.release()

    #######################################
    #Read from usb webcam
    #######################################
    cap = ipcamCapture("rtsp://your URL")
    #cap = ipcamCapture(0)

    # thread frame start
    cap.start()

    # pause for 1 second to make sure image buffer filled.
    time.sleep(1)
    #######################################
    #Set connection ip to jetson device
    #######################################
    try:
        with open(r'setting\settings.json', 'r') as f:
            data = json.load(f)
        xavierurl = data['jetson_ip']
        print('calling faceAI======'+xavierurl)
    except:
        xavierurl = 'http://192.168.1.84:8001/upload'
    
    ###############################################################################
    #Crop optical camera image so that it is the same as its thermal counterpart
    #Initialize cropping parameters
    ###############################################################################
    yminc = 0
    ymaxc = 720
    xminc = 0
    xmaxc = 1280

    while True:
    
        ##################################################################    
        ##Thermal camera acquisition using mvIMPACT
        ##################################################################
               ##################################################################
        
        ##################################################################
        #Crop optical camera image so that it is the same as its thermal counterpart
        ###########################################################################
        
        try:
            with open(r'setting\settings.json', 'r') as f:
                data = json.load(f)
            yminc = data['ymin']
            ymaxc = data['ymax']
            xminc = data['xmin']
            xmaxc = data['xmax']
            #print('calling faceAI======'+ymaxc)
        except:
            yminc = yminc
            ymaxc = ymaxc
            xminc = xminc
            xmaxc = xmaxc
        ##################################################################
        # Capture frame-by-frame
        ##################################################################
        st = time.time()
        frame = cap.getframe()
        ####################################################################################################################################
        #Crop optical camera image so that it is the same as its thermal counterpart
        ####################################################################################################################################
        frame = frame[yminc:ymaxc, xminc:xmaxc]

        ####################################################################################################################################
        #Encode optical images as base64 string for webapi transfer to jetson device for facial mask inference task.
        ####################################################################################################################################
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        #print("ready to call the faceAPI POST")
        r = requests.post(xavierurl, data=jpg_as_text)
        results = json.loads(r.text)
        array = results['data']

        #############################################################################################################################################
        ##Store the resulting bounding boxes and mask detection results into a bounding box array and mask array for overlaying on image frames.
        #############################################################################################################################################
        for idx in range(len(array)):
            ID = array[idx]['class_id']
            xmin = array[idx]['xmin']
            ymin = array[idx]['ymin']
            xmax = array[idx]['xmax']
            ymax = array[idx]['ymax']
            if ID == 'NoMask':
                color = (0,0,255)
            elif ID == 'Mask':
                color = (255,0,0)
            else:
                color = (0,255,0)
            #############################################################################################################################################
            ##Using boundingboxes found with facial mask detection earlier to crop thermal images for optimal temperature data associated with each face.
            #############################################################################################################################################
            #max_temp = np.amax(thermal_img[ymin:ymax, xmin:xmax])
            #max_temp = (max_temp/100) - 273.15
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 4)
            cv2.rectangle(frame, (xmin, ymin-45), (xmin+110, ymin-5), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, ID, (xmin, ymin - 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)
            #cv2.putText(frame, str.format('[%.2f]' % 37), (xmin, ymin - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)

        ##################################################################
        # Display the resulting frame on a webpage using html
        ##################################################################
        frame = cv2.resize(frame, (1280,720))
        ret, jpeg = cv2.imencode('.jpg', frame)
        htmlimage = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + htmlimage + b'\r\n\r\n')

        ##################################################################
        # When everything is done, release the capture
        ##################################################################
        #cap.releases()
        if cv2.waitKey(50) == 27:    
            cv2.destroyAllWindows()
            cap.stop()

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port='8432', debug=True)




