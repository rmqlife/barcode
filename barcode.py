# reference:
# http://www.pyimagesearch.com/2014/11/24/detecting-barcodes-images-python-opencv/
import cv2
import numpy as np
class barcode:
    def detect(self,img,debug=False):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # compute the Scharr gradient magnitude representation of the images in x and y direction
        # ksize = -1 <--> Scharr 
        gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
        gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
        
        # substract the y-gradient from x-gradient
        gradient = cv2.subtract(gradX, gradY)
        # convert scale of color
        gradient = cv2.convertScaleAbs(gradient)
        if (debug):
            cv2.imshow('gradient', gradient)

        
        # blur and threshold
        # blur help remove high frequency noise
        blur = cv2.blur(gradient, (9,9))
        ret, thresh  = cv2.threshold(blur, 225, 255, cv2.THRESH_BINARY)
        if (debug):
            cv2.imshow('thresh', thresh)
        
        # morphological
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21,7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        if (debug):
            cv2.imshow('closed', closed)
        
        # remove small blobs
        closed = cv2.erode(closed, None, iterations = 4)
        closed = cv2.dilate(closed, None, iterations = 4)
        if (debug):
            cv2.imshow('erode and dilate', closed)
        
        # find contours 
        _, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # sort by area, maxArea
        c = sorted(cnts, key =  cv2.contourArea, reverse = True)[0]
        # to Rectangle
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))
        
        if (debug):
            cv2.drawContours(img,[box],-1,(0,255,0),3)
            cv2.imshow("rect", img)
                    
        if (debug):
            cv2.waitKey()
if __name__ == "__main__" :
    img = cv2.imread('code0.jpg')
    barcode().detect(img,1)
    

