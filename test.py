#! /usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from utils.defisheye import Defisheye
from utils import range_finder as rf
from cv_bridge import CvBridge
import time
import yaml
import os

img = None


def getImage(im):
    global img
    img = im


rospy.init_node('test')
sub_image = rospy.Subscriber('/usb_cam/image_raw', Image, getImage, queue_size=1)
defisheye = Defisheye(dtype='linear', format='fullframe', fov=160, pfov=130)
bridge = CvBridge()
# Loading configs from config.yaml
path = os.path.dirname(os.path.abspath(__file__))
with open(path + '/config.yml', 'r') as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)
real_ttb = rf.RealTtb(config, output=(800, 800))

while True:
    if img is not None:
        frame = bridge.imgmsg_to_cv2(img, desired_encoding='passthrough')
        frame = frame[:, 0:round(frame.shape[1]*0.9)]
        frame = defisheye.convert(frame)
        angle, distance, frame = real_ttb.get_angle_distance(frame, 1.0)
        print('Angle:', angle, 'Distance:', distance)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    time.sleep(0.05)
