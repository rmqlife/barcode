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
        for y in xrange(rows):
            for x in xrange(cols):
                roi = img[y*bh:y*bh+bh,x*bw:x*bw+bw]
                white = cv2.countNonZero(roi)
                v = int(white > (bw*bh/2))
                mat[y,x] = v
        return mat
          
    # hamming2d 5*5, num [0, 1023]
    def encode(self, num, blocksize =50):
        # create an instance of class hamming2d
        h2d = hamming.hamming2d()
        hlist = h2d.encode(num)
        mat = self.strlist2mat(hlist)        
        return self.mat2img(mat)   
    
    # hamming2d 5*5 decode
    def decode(self, img, debug = False):
        mat = self.img2mat(img,7,7)
        # remove the border
        mat = mat[1:-1,1:-1]
        # create an instance of hamming2d
        h2d = hamming.hamming2d()
        # rotate the mat to find the right code
        for i in xrange(4):
            ret,num = h2d.decode(self.mat2strlist(mat))
            if debug:
                print ret,num
            elif ret == True:
                return ret, num
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
        
    def strlist2mat(self, strlist):
        mat = []
         # h is a string
        for h in strlist:
            mat.append( [int(i) for i in h] )
        return mat
    
    # find all the marker candidates in an raw image, BGR
    def find(self, img, debug = False, show = False):
        """return a list of (num,position) """
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #ret2, bw = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
        bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                    cv2.THRESH_BINARY, 101, 7)
        if debug:            
            cv2.imshow("bw",np.hstack([gray,bw]))
            
        _, cnts, _ = cv2.findContours(bw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)        
        # remove small ones
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
        # find polygons have 4 laterals        
        poly4s = []
        for c in cnts:
            peri =  cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                poly4s.append(approx)
        if debug:
            cv2.drawContours(img, poly4s, -1, (255,0,0), 2)
        
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
            
        if debug:
            show = []
            # horizontal stack warps 
            for candidate in candidates:
                pic,position = candidate
                show.append(pic)
            cv2.imshow("warp",np.hstack(show))
        
        # decode
        result = list()
        for candidate in candidates:
            pic, position = candidate
            ret, num =  self.decode(pic)
            if ret:
                result.append((num,position))            
           
        if debug:
            cv2.waitKey(0)
            
        if show:
            for num, position in result:
                cv2.drawContours(img, [position], -1, (0,255,0), 2)
                # vertical mean
                textpos = tuple(np.int0( np.mean(position.reshape(4,2), axis = 0)))
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,str(num),textpos, font, 1,(255,255,0),2,cv2.LINE_AA)
            return img
        else:    
            return result
        
                
if __name__ == "__main__":
    if False:
        img = marker().mat2img([[1,1],[0,1],[1,1]],100)    
        cv2.imshow("img",img)
        print marker().img2mat(img,5,4)
        cv2.waitKey(0)
        
    if False:
        import sys
        print sys.argv
        num = 0
        if len(sys.argv)>1:    
            num = int(sys.argv[1])

        img2 = marker().encode(num)
        cv2.imshow("img",img2)
        print marker().decode(img2)
        cv2.waitKey(0)
        
        if len(sys.argv)>2:
            fn = sys.argv[2]
            cv2.imwrite(fn,img2)  
            
    if True:
        import sys
        print sys.argv
        if len(sys.argv)>1:
            fn = sys.argv[1]
            img = cv2.imread(fn)
            show = marker().find(img,debug = 0, show = 1)
            cv2.imshow("show",show)
            cv2.waitKey(0)
            
    if False:
        import sys
        print sys.argv
        if len(sys.argv)>1:
            fn = sys.argv[1]
            img = cv2.imread(fn,0)
            marker().decode(img)
