import cv2
from faceDetector import face_detector
from faceRecognition import face_recognition
  
# define a video capture object
vid = cv2.VideoCapture(0)

face_detector = face_detector.FaceDetection()
face_recognition = face_recognition.FaceNet(detector=face_detector,threshold= 0.4)
  
while(True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    face_recognition(frame=frame)
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()