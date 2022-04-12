from logging import exception
from pydoc import classname
import cv2
import sys
import time

output_stream = sys.stdout

thres = 0.45 # Threshold to detect object

cap = cv2.VideoCapture("DATA/1.mp4")
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)
out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))

#classNames= []
classFile = 'ObjDetection/coco.names'
with open(classFile,'rt') as f:
    print(f)
    classNames = f.read().splitlines()
    #classNames = f.read().rstrip('n').split('n')

configPath = 'ObjDetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'ObjDetection/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

counter = 0
detected_objects = []
while cap.isOpened():
    success,img = cap.read()

    if success is True:
        classIds, confs, bbox = net.detect(img,confThreshold=thres)


        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):   
                cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                if classNames[classId-1] in detected_objects:
                    detected_objects
                else:
                    detected_objects.append(classNames[classId-1])
                    
                try:
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                except:
                    print("An exception occurred") 
                cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

        cv2.imshow("Output",img)
        out.write(img)
        cv2.waitKey(1)
        output_stream.write('Frame: ' + str(counter) + '\n Detected Objects: ' + str(detected_objects) + "\n")
        output_stream.flush()
        output_stream.write("\n")
        counter += 1
    cap.release()
    out.release()