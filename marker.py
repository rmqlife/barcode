import cv2
import numpy as np
import hamming

class marker:
    # mat2img a marker by mat, mat is a 2d list  
    def mat2img(self, mat, blocksize = 50):
        #expand mat with 0
        center = np.array(mat)
        mat = np.int0(np.zeros((center.shape[0]+2, center.shape[1]+2)))
        mat[1:-1,1:-1] = center
        
        for i in xrange(mat.shape[0]):
            for j in xrange(mat.shape[1]):
                v = mat[i,j] * 255
                b = np.ones([blocksize,blocksize]) * v
                if j == 0:
                    row = b
                else:
                    row = np.append(row, b, 1)
            if i == 0:
                img = row
            else: 
                img = np.append(img, row, 0)
        return img        
    
    # 5*5 block decode
    # binary image, rows, cols
    def img2mat(self,img,rows,cols):
        h,w = img.shape[:2]
        # height of block
        bh = h/rows
        # width of block
        bw = w/cols
        mat = np.int0(np.zeros((rows,cols)))
               
        for y in range(0,h,bh):
            for x in range(0,w,bw):
                roi = img[y:y+bh,x:x+bw]
                white = cv2.countNonZero(roi)
                v = int(white > (bw*bh/2))
                mat[y/bh,x/bw] = v
        return mat
          
    # hamming2d 5*5, num [0, 1023]
    def encode(self, num, blocksize =50):
        # create an instance of class hamming2d
        h2d = hamming.hamming2d()
        hlist = h2d.encode(num)
        mat = self.strlist2mat(hlist)        
        return self.mat2img(mat)   
    
    # hamming2d 5*5 decode
    def decode(self, img):
        mat = self.img2mat(img,7,7)
        # remove the border
        mat = mat[1:-1,1:-1]
        # create an instance of hamming2d
        h2d = hamming.hamming2d()
        # rotate the mat to find the right code
        for i in xrange(4):
            ret,num = h2d.decode(self.mat2strlist(mat))
            if ret == True:
                return ret,num
            mat = np.rot90(mat)
        return False, -1
    
    # tranfer np.array to a string list   
    def mat2strlist(self, mat):
        # array to list
        mat = mat.tolist()
        matstr = []
        # transfer mat to a string vector
        for row in mat:
            s = ""
            for i in row:
                s += str(i)    
            matstr.append(s)
        return matstr
        
    def strlist2mat(self,strlist):
        mat = []
         # h is a string
        for h in strlist:
            mat.append( [int(i) for i in h] )
        return mat
            
if __name__ == "__main__":
    if False:
        img = marker().mat2img([[1,1],[0,1],[1,1]],100)    
        cv2.imshow("img",img)
        print marker().img2mat(img,5,4)
        cv2.waitKey(0)
    
    img2 = marker().encode(0)
    cv2.imshow("img",img2)
    print marker().decode(img2)
    cv2.waitKey(0)
    
