import cv2
import os

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

# # Set the location of the frames
# frame_folder = 'outputs/'

# # Loop through all the frames
# for i in range(0, len(os.listdir(frame_folder))):
#     filename = frame_folder +"output"+ str(i) + '.jpg'
#     frame = cv2.imread(filename)

#     # Write the frame
#     out.write(frame)

# # Release the video writer
# out.release()


def SaveVideo(filename = 'video.mp4'):
    frame_folder = 'output/'
    w = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (1920, 1080))
    for i in range(0, len(os.listdir(frame_folder))):
      filename = frame_folder +"output"+ str(i) + '.jpg'
      frame = cv2.imread(filename)
      # Write the frame
      w.write(frame)
    w.release()

SaveVideo()