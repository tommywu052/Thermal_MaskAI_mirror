
import json
import os
import io
import time

# Imports for the REST API
from flask import Flask, request, jsonify, Response

# Imports for image procesing
from PIL import Image

app = Flask(__name__)

@app.route('/WebService/RecieveCoordinate', methods=['POST'])
def get_max_temp():
    max_temp_array = []
    
    data = json.loads(request.data.decode())
    num_masks = data['Mask']

    for idx in range(len(num_masks)):
        max_temp_array.append(37.23)
    reply = {'ReturnCode': '0','Data': {'MaxTemperature':max_temp_array}}
    
    return Response(json.dumps(reply), mimetype='application/json')
    # return Response(reply, mimetype='multipart/form-data')

if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=8066)

