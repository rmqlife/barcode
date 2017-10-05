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
from marker_pnp import *
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

def process_rgb(msg):
    bridge = CvBridge()
    global have_im; have_im = True
    global im; im = bridge.imgmsg_to_cv2(msg)

if __name__ == '__main__':
    publisher = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)


    fn = './data/marker.jpg'
    img = cv2.imread(fn)
    objp_test, objp = find_position(img)
    
        
    while not rospy.is_shutdown():
       # Renumber the marker IDs
       # Publish the MarkerArray
       
        markerArray = MarkerArray()
        
        for i in range(objp_test.shape[0]):
           marker = show_marker(objp_test[i,0],objp_test[i,1],0)
           markerArray.markers.append(marker)
        
        for i in range(objp.shape[0]):
           marker = show_marker(objp[i,0],objp[i,1],0)
           markerArray.markers.append(marker)
        
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1

        publisher.publish(markerArray)
        rospy.sleep(1)
