import qrcode
import matplotlib.pyplot as plt
import cv2
import numpy as np

def find_transform(imgp,imgp_test):
    w = 0.3
    # object points
    imgp = np.float32(np.array([imgp]))
    imgp_test =np.float32(np.array([imgp_test]))
    objp = np.array([[0,0],[0,w],[w,0],[w,w]], dtype = "float32")

    #m = cv2.getPerspectiveTransform(imp,objp)
    m,_ = cv2.findHomography(imgp,objp)
    
    objp_test = cv2.perspectiveTransform(imgp_test,m)
    
    objp_test = objp_test.reshape(-1,2)
    objp = objp.reshape(-1,2)
    return objp_test, objp

def find_position(img):
    res = qrcode.marker().find(img,debug = 0, show = 0)
    scale = 1.0
    centers = np.zeros((10,2))
    corners = np.zeros((10,2*4))
    for r in res:
        code = r[0]
        pos = r[1].reshape(4,2)
        pos = np.float32(pos)
        pos[:,0] = pos[:,0]/scale
        pos[:,1] = pos[:,1]/scale

        center = np.mean(pos,axis=0)
        centers[code] = center
        corners[code] = pos.reshape(1,-1)
    # image points
    objp_test,objp = find_transform(centers[:4],centers[4:6])
    return objp_test,objp

if __name__ == '__main__':
    fn = './data/marker.jpg'
    img = cv2.imread(fn)
    plt.imshow(img,cmap='gray'); plt.show()
    p1,p2 = find_position(img)
    print p1
    print p2
