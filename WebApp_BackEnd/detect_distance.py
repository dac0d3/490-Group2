import cv2
import pyrealsense2
from realsense_depth import *
import os
import datetime
import subprocess

class RS_Camera: #real sense camera


    def __init__(self):
        #Initialize Camera Intel RealSense
        self.intelImages = intelImages = "astrocultivators/static/images/rgb"
        if not os.path.exists(intelImages):
            os.makedirs(intelImages)

        self.intelImagesDepth = intelImagesDepth = "astrocultivators/static/images/depth"
        if not os.path.exists(intelImagesDepth):
            os.makedirs(intelImagesDepth)

        self.dc = DepthCamera() #initialize camera
        self.rgb_filename = None
        self.depth_filename = None

    # Take Picture
    def take_picture(self):
        count = 0

        while count == 0 :
            self.ret, self.depth_frame, self.rgb_frame = self.dc.get_frame()
            filename_sub=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            #rgb_frame,depth_frame = dc.get_frame()
            self.rgb_filename=os.path.join(self.intelImages,f"rgb_{filename_sub}.png")
            cv2.imwrite(self.rgb_filename,self.rgb_frame)

            #save depth image with timestamp
            self.depth_filename=os.path.join(self.intelImagesDepth,f"depth_{filename_sub}.png")
            cv2.imwrite(self.depth_filename, self.depth_frame)

            obj_det_source = f"rgb_{filename_sub}.png"
            self.object_detection(obj_det_source)
            count = 1
        
        self.dc.release()

    def object_detection(self,fileName):
        
        # Define paths
        project_directory = "/home/orin/AstroCultivatorNew/AstroCultivators/yolov7-custom"
        virtualenv_activate_script = "/home/orin/AstroCultivatorNew/AstroCultivators/yolov7-custom/yolov7_custom/bin/activate"
        object_detection_script = f"python detect.py --weights yolov7_custom.pt --conf 0.5 --img-size 640 --source {fileName} --view-img --no-trace --save-txt"

        # Command to activate virtual environment and run object detection script
        command = [
            f"cd {project_directory} &&",  # Change directory
            f". {virtualenv_activate_script} &&",  # Activate virtual environment
            object_detection_script,  # Run object detection script
        ]

        # Run the command as a subprocess
        subprocess.run(" ".join(command), shell=True)


    def output_distance(self, x, y,):
        #Show distance for a specific point
        sizeX = len(x)
        z = []

        for i in range(sizeX):
            point =x[i],y[i]
            #cv2.circle(self.rgb_frame, point, 4, (0, 0, 255))
            distance = self.depth_frame[point[1], point[0]]

            z.append(distance)         
            
        #rewrite z values to file to do

    def read_coordinates(self,fileDateTime):
        with open (f"rgb_{fileDateTime}.txt", "r") as file:
            lines=file.readlines()
            x_coords=[]
            y_coords=[]

            modifiedlines= [line[1:].lstrip for line in lines]
            for line in modifiedlines:
                parts = line.split()
                x_coord= int(parts[0])
                y_coord= int(parts[1])

                x_coords.append(x_coord)
                y_coords.append(y_coord)
            
        self.output_distance(x_coords,y_coords)


    #cv2.waitKey(0)
    #key = cv2.waitKey(1)

