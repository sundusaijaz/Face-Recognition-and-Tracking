import cv2
from yoloseg import YOLOSeg
from yoloseg.utils import class_names
from yolov8 import YOLOv8
from yolov8.Tracker import Tracker
from yolov8.utils import class_names
import torch
from object_tracker.tracker import create_tracker
import numpy as np
from faceDetector import face_detector
from faceRecognition import face_recognition
import time
id_face_dictionary = {}


font = cv2.FONT_HERSHEY_DUPLEX
tracker = create_tracker("object_tracker/cfg/ocsort.yaml")


face_detector = face_detector.FaceDetection()
face_recognition = face_recognition.FaceNet(detector=face_detector,threshold=0.4)


model_path = "models/Detection/yolov8n.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.3, iou_thres=0.5)

run_bject_detection = True

start_time_sec = 15
start_time_msec = start_time_sec * 1000
SECONDS_TO_CHECK = 2

vid = cv2.VideoCapture('sample.mp4')

class GetProcessingFps():
    def __init__(self,rate=1):
        self.processing_rate = rate
obj=GetProcessingFps()

def run_webcam():
    vid.set(cv2.CAP_PROP_POS_MSEC, start_time_msec)
    count = 0
    start = time.time()
    while(True):
        ret, frame = vid.read()
        
        if run_bject_detection == True:
            frame = cv2.resize(frame,(500,300))
            modl = object_detection_(frame)
            if modl is None:
                modl = frame
        else:
            modl = frame
        #modl = cv2.resize(modl,(500,500))
        abs_time = (time.time()-start)
        if round(abs_time) > 1:
            start = time.time()
            obj.processing_rate = round(abs_time)
        cv2.imshow('frame', modl)
        # cv2.imwrite(f"output/output{count}.jpg",modl)
        # count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release()

    cv2.destroyAllWindows()




def drawPerson(frame,bbox_left,bbox_top,bbox_w,bbox_h,class_,id,tracked_name):
    linewidth = 30  
    cv2.rectangle(frame, (bbox_left, bbox_top),(bbox_w, bbox_h), (0, 0, 255), 2)
    cv2.putText(frame, f"{tracked_name} ID: {id}", (bbox_left, bbox_top), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
    # ###### Top Left
    # cv2.line(frame,(bbox_left, bbox_top),(bbox_left+linewidth, bbox_top),(0, 0, 255),thickness=5)
    # cv2.line(frame,(bbox_left, bbox_top),(bbox_left, bbox_top+linewidth),(0, 0, 255),thickness=5)
    # ###### Top Right
    # cv2.line(frame,(bbox_left+bbox_w, bbox_top),(bbox_left+ bbox_w -linewidth, bbox_top),(0, 0, 255),thickness=5)
    # cv2.line(frame,(bbox_left+bbox_w, bbox_top),(bbox_left+ bbox_w, bbox_top +linewidth),(0, 0, 255),thickness=5)
    # ###### Bottom Left
    # cv2.line(frame,(bbox_left, bbox_top+bbox_h),(bbox_left+linewidth, bbox_top+bbox_h),(0, 0, 255),thickness=5)
    # cv2.line(frame,(bbox_left, bbox_top+bbox_h),(bbox_left, bbox_top+bbox_h -linewidth),(0, 0, 255),thickness=5)
    # ###### Bottom Right
    # cv2.line(frame,(bbox_left+bbox_w, bbox_top+bbox_h),(bbox_left+ bbox_w -linewidth, bbox_top+bbox_h),(0, 0, 255),thickness=5)
    # cv2.line(frame,(bbox_left+bbox_w, bbox_top+bbox_h),(bbox_left+ bbox_w, bbox_top+bbox_h -linewidth),(0, 0, 255),thickness=5)

def modify_to_positive(value):
    return int(abs(value))



informations = []

def ids_checks(id_face_dictionary_temp):
    ls = []
    not_in = []
    for i in informations:
        for j in i:
            if i not in ls:
                ls.append(j)
    keys = [i for i in id_face_dictionary_temp]
    for k in list(keys):
        print(k)
        if k not in ls:
            print(id_face_dictionary)
            print(f"removing --> {id_face_dictionary_temp[k]}")
            del(id_face_dictionary[k])
            print(id_face_dictionary)
    return id_face_dictionary


def object_detection_(frame):
    global id_face_dictionary
    global informations
    PREVIOUS_FRAMES_TO_CHECK = round(obj.processing_rate*SECONDS_TO_CHECK)
    #print(PREVIOUS_FRAMES_TO_CHECK, obj.processing_rate,SECONDS_TO_CHECK)
    boxes, scores, class_ids = yolov8_detector(frame)
    ls = []
    list = []
    if len(boxes) > 0:
        for location,id_,score in zip(boxes, class_ids, scores):
            ls.append([location[0],location[1],location[2],location[3], score, id_])
        ls = torch.tensor(ls).cpu()   
        data = tracker.update(ls)
        id = 'none'
        flag = False
        for output in zip(data):  
            
            output = output[0]
            bbox_left = modify_to_positive(output[0])
            bbox_top = modify_to_positive(output[1])
            bbox_w = modify_to_positive(output[2]) 
            bbox_h = modify_to_positive(output[3])
            id = int(output[4])
            class_ = int(output[5])
            if class_names[class_].lower() == 'person':
                if bbox_w > 0 and bbox_h > 0:
                    person_frame = frame[bbox_top:bbox_h,bbox_left:bbox_w,:]
                    name = face_recognition(frame=person_frame)
                    if bool(name):
                        print(name)
                        list.append(id)
                        flag = True
                        if id not in id_face_dictionary and name not in id_face_dictionary.values():
                            name = name
                            id_face_dictionary[id] = name
                            tracked_name = name
                            drawPerson(frame,bbox_left,bbox_top,bbox_w,bbox_h,class_,id,tracked_name)                  
                if id in id_face_dictionary:
                    tracked_name = id_face_dictionary[id] 
                    drawPerson(frame,bbox_left,bbox_top,bbox_w,bbox_h,class_,id,tracked_name)  
            #else:
                    # cv2.rectangle(frame, (bbox_left, bbox_top),(bbox_w, bbox_h), (0, 0, 255), 1)
                    # cv2.putText(frame, f"Class:{class_names[class_]} ID:{id} ", (bbox_left, bbox_top), font, 0.5, (0, 0, 255), 1)
            
        '''
        check mark 1.0
        '''
        if flag == False:
            list.append(id)
        informations.append(list)
        informations = informations[-PREVIOUS_FRAMES_TO_CHECK:]
        if id_face_dictionary:
            id_face_dictionary = ids_checks(id_face_dictionary) 
        return frame

run_webcam()