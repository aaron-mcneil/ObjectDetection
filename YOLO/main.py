import cv2
import numpy as np
#import requests

#url = "http://192.168.1.121:4747/video"

#net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
#net = cv2.dnn.readNet('yolov3small.weights', 'yolov3small.cfg')
net = cv2.dnn.readNet('yolov3tiny.weights', 'yolov3tiny.cfg')
classes = []
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture("http://192.168.1.121:4747/video")
#img = cv2.imread('image.jpg')
font = cv2.FONT_HERSHEY_PLAIN

while True:
    _, img = cap.read()
    #img_resp = requests.get(url)
    #img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    #img = cv2.imdecodeimg_arr, -1
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416,416), (0,0,0), swapRB=True, crop=False)

    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x-w/2)
                y = int(center_y-h/2)

                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    #colors = np.random.uniform(0,255,size=(len(boxes), 3))

    if len(indexes) != 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            #color = colors[i]
            color = (0,255,0)
            cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y+20), font, 1, color, 1)

    cv2.imshow('Output', img)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
