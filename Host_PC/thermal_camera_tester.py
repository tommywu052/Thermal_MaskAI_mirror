from __future__ import print_function
import os
import platform
import string
import sys
# import all the stuff from mvIMPACT Acquire into the current scope
from mvIMPACT import acquire
# import all the mvIMPACT Acquire related helper function such as 'conditionalSetProperty' into the current scope
# If you want to use this module in your code feel free to do so but make sure the 'Common' folder resides in a sub-folder of your project then
from mvIMPACT.Common import exampleHelper
 
# For systems with NO mvDisplay library support
import ctypes
from PIL import Image
import numpy as np
import cv2
 
devMgr = acquire.DeviceManager()
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
 
exampleHelper.manuallyStartAcquisitionIfNeeded(pDev, fi)

while True:

    requestNr = fi.imageRequestWaitFor(10000)
    if fi.isRequestNrValid(requestNr):
        pRequest = fi.getRequest(requestNr)
        
        if pRequest.isOK:
            # For systems with NO mvDisplay library support
            cbuf = (ctypes.c_char * pRequest.imageSize.read()).from_address(int(pRequest.imageData.read()))
            channelType = np.uint16 if pRequest.imageChannelBitDepth.read() > 8 else np.uint8
            thermal_img = np.fromstring(cbuf, dtype = channelType)
            thermal_img.shape = (pRequest.imageHeight.read(), pRequest.imageWidth.read(), pRequest.imageChannelCount.read())
            cv2.imshow('thermal', thermal_img)

        if pPreviousRequest != None:
            pPreviousRequest.unlock()
        pPreviousRequest = pRequest
        fi.imageRequestSingle()
    
    else:
        print("imageRequestWaitFor failed (" + str(requestNr) + ", " + acquire.ImpactAcquireException.getErrorCodeAsString(requestNr) + ")")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()