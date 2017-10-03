#!/usr/bin/env python
# Software License Agreement (BSD License)
import sys
import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge
import cv2
import qrcode


import roslib
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import math



def process_rgb(msg):
    bridge = CvBridge()
    global have_im; have_im = True
    global im; im = bridge.imgmsg_to_cv2(msg)


def find_marker(img):
    result = qrcode.marker().find(img,debug = 0, show = 0)
    return result

def show_marker(x,y,z):
    print("marker to show",x,y,z)
    marker = Marker()
    # this frame_id can only be map!
    marker.header.frame_id = "map"
    marker.type = marker.CUBE
    marker.action = marker.ADD
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.2
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.pose.orientation.w = 1.0
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z
    return marker

def transform():
    # warp candidates
    W = 100
    target = np.array([[0,0],[W,0],[W,W],[0,W]], dtype = "float32")
    candidates = []
    
    for poly4 in poly4s:
        # remove brackets
        position = poly4.copy()
        poly4 = np.float32(poly4.reshape(4,2))
        # poly4, target need to be float32
        M = cv2.getPerspectiveTransform(poly4,target) 
        candidate = (cv2.warpPerspective(bw, M, (W,W)), position)
        candidates.append(candidate)


if __name__ == '__main__':
    publisher = rospy.Publisher('visualization_marker_array', MarkerArray,queue_size=10)
    rospy.init_node('talker', anonymous=True)

        
    while not rospy.is_shutdown():
       # Renumber the marker IDs
       # Publish the MarkerArray
       
        markerArray = MarkerArray()
            
        fn = './data/set1.jpg'
        img = cv2.imread(fn)
        res = find_marker(img)
        scale = 1000.0
        for r in res:
            code = r[0]
            pos = r[1].reshape(4,2)
            pos = np.float32(pos)
            pos[:,0] = pos[:,0]/scale
            pos[:,1] = pos[:,1]/scale

            center = np.mean(pos,axis=0)
            print code,center
            marker = show_marker(center[0],center[1],0)
            markerArray.markers.append(marker)

        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1

        publisher.publish(markerArray)
        rospy.sleep(1)