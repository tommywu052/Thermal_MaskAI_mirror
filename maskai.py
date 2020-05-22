#!/usr/bin/env python
# coding: utf-8
import cv2, base64
import numpy as np
import requests
import json
import queue, threading
from flask import jsonify, Flask, render_template, Response
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
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

    cap = VideoCapture(0)

    xavierurl = 'http://192.168.99.95:8001/upload'
    max_temp_array = []
    
    # yminc = 200
    # ymaxc = 440
    # xminc = 500
    # xmaxc = 840
    yminc = 0
    ymaxc = 720
    xminc = 0
    xmaxc = 1280
    while True:
        try:
            with open(r'setting\settings.json', 'r') as f:
                data = json.load(f)
            yminc = data['ymin']
            ymaxc = data['ymax']
            xminc = data['xmin']
            xmaxc = data['xmax']
        except:
            yminc = yminc
            ymaxc = ymaxc
            xminc = xminc
            xmaxc = xmaxc
        # Capture frame-by-frame
        st = time.time()
        frame = cap.read()
        frame = frame[yminc:ymaxc, xminc:xmaxc]
        # ##Tell ThermalCam to grab
        try:
            r = requests.get('http://127.0.0.1' + ':8066/WebService/GrabTrigger?Grab=true')
        except:
            pass

        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        r = requests.post(xavierurl, data=jpg_as_text)
        results = json.loads(r.text)
        array = results['data']

        bbox = []
        colors = []
        maskresults = []
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
            singlebox = {"Left":str(xmin),"Top":str(ymin),"Right":str(xmax),"Bottom":str(ymax)}
            bbox.append(singlebox)
            colors.append(color)
            maskresults.append(ID)

        ##Code modifications below
        ##########################
        max_temp_array = max_temp_array
        try:
            # print(maskresults)
            ## Sending BoundingBoxes to ThermalCam####
            jsondata = {"BoundingBox": bbox, "Mask": maskresults}
            json_data = json.dumps(jsondata)
            url = "http://127.0.0.1" + ":8066/WebService/RecieveCoordinate"
            r = requests.post(url = url, data = json_data)
            POST_response = r.text
            json_response = json.loads(POST_response)
            returncode = json_response["ReturnCode"]
            if returncode is '0':
                temp_data = json_response["Data"]
                max_temp_array = temp_data["MaxTemperature"]
            else:
                pass
        except:
            pass

        ##Draw array of bounding boxes
        ##############################
        for i in range(len(max_temp_array)):
            try: 
                onebox = bbox[i]
                xmin, ymin, xmax, ymax = np.int(onebox['Left']), np.int(onebox['Top']), np.int(onebox['Right']), np.int(onebox['Bottom'])
                masked = maskresults[i]
                max_temp = max_temp_array[i]
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), colors[i], 4)
                cv2.rectangle(frame, (xmin, ymin-45), (xmin+110, ymin-5), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, masked, (xmin, ymin - 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, colors[i], 1)
                cv2.putText(frame, str.format('[%.2f]' % max_temp), (xmin, ymin - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, colors[i], 1)
            except:
                pass


        # Display the resulting frame
        # cv2.imshow('Video', frame)
        frame = cv2.resize(frame, (960,720))
        ret, jpeg = cv2.imencode('.jpg', frame)
        htmlimage = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + htmlimage + b'\r\n\r\n')

        print("CT: " + str(time.time()-st))
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # When everything is done, release the capture
    cap.releases()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port='8432', debug=True)




