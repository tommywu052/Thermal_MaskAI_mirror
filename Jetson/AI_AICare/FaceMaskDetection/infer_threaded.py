# -*- coding:utf-8 -*-
import cv2, queue, threading
import time
from datetime import datetime
import argparse
from flask import jsonify, Flask, render_template, Response, request
import json
import base64

import numpy as np
from PIL import Image
from keras.models import model_from_json
from utils.anchor_generator import generate_anchors
from utils.anchor_decode import decode_bbox
from utils.nms import single_class_non_max_suppression
from load_model.keras_loader import load_keras_model, keras_inference

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)

model = load_keras_model('/home/smasoft/AI_AICare/FaceMaskDetection/models/face_mask_detection.json', '/home/smasoft/AI_AICare/FaceMaskDetection/models/face_mask_detection.hdf5')

# anchor configuration
feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
anchor_ratios = [[1, 0.62, 0.42]] * 5

# generate anchors
anchors = generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)

# for inference , the batch size is 1, the model output shape is [1, N, 4],
# so we expand dim for anchors to [1, anchor_num, 4]
anchors_exp = np.expand_dims(anchors, axis=0)

id2class = {0: 'Mask', 1: 'NoMask'}

def inference(image,
              conf_thresh=0.5,
              iou_thresh=0.4,
              target_shape=(160, 160),
              draw_result=True,
              show_result=True):
    '''
    Main function of detection inference
    :param image: 3D numpy array of image
    :param conf_thresh: the min threshold of classification probabity.
    :param iou_thresh: the IOU threshold of NMS
    :param target_shape: the model input size.
    :param draw_result: whether to daw bounding box to the image.
    :param show_result: whether to display the image.
    :return:
    '''
    # image = np.copy(image)
    output_info = []
    height, width, _ = image.shape
    image_resized = cv2.resize(image, target_shape)
    image_np = image_resized / 255.0  
    image_exp = np.expand_dims(image_np, axis=0)

    y_bboxes_output, y_cls_output = keras_inference(model, image_exp)
    # remove the batch dimension, for batch is always 1 for inference.
    y_bboxes = decode_bbox(anchors_exp, y_bboxes_output)[0]
    y_cls = y_cls_output[0]
    # To speed up, do single class NMS, not multiple classes NMS.
    bbox_max_scores = np.max(y_cls, axis=1)
    bbox_max_score_classes = np.argmax(y_cls, axis=1)

    # keep_idx is the alive bounding box after nms.
    keep_idxs = single_class_non_max_suppression(y_bboxes,
                                                 bbox_max_scores,
                                                 conf_thresh=conf_thresh,
                                                 iou_thresh=iou_thresh,
                                                 )

    for idx in keep_idxs:
        conf = float(bbox_max_scores[idx])
        class_id = bbox_max_score_classes[idx]
        bbox = y_bboxes[idx]
        # clip the coordinate, avoid the value exceed the image boundary.
        xmin = max(0, int(bbox[0] * width))
        ymin = max(0, int(bbox[1] * height))
        xmax = min(int(bbox[2] * width), width)
        ymax = min(int(bbox[3] * height), height)
        
        js = {"class_id": id2class[class_id], "conf": str(conf), "xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax}
        output_info.append(js)

    jsonresult = {"data": output_info}
    if show_result:
        Image.fromarray(image).show()
    return jsonresult

## Bufferless VideoCapture
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
                    self.q.get_nowait() # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()
    
    def releases(self):
        self.cap.release()

@app.route("/upload", methods=['POST'])
def inf_loop():
    output_info = []
    idx = 0
    st = time.time()
    start_stamp = time.time()

    jpg_original = base64.b64decode(request.data)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img_raw = cv2.imdecode(jpg_as_np, flags=1)
    img_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)

    ## Do MaskAI to get mask result
    jsonresult = inference(img_raw, conf_thresh=0.5, iou_thresh=0.5, target_shape=(260, 260), draw_result=True, show_result=False)

    return Response(json.dumps(jsonresult), mimetype = 'application/json')
    #cap.releases()


if __name__ == "__main__":
    
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8001, address="0.0.0.0")
    print("FaceMask Detection Server is on!")

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()
    #inf_loop()
