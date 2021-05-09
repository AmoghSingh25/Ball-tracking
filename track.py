import cv2
import numpy as np
import imutils

def position(x,y,h,w):
    s=''
    if(y<h/2):
        s+='top'
    else:
        s=s+'bottom'
    if(x>w/2):
        s=s+'-right'
    else:
        s=s+'-left'
    return s


def ret_im(img):
    h,w,c=img.shape #X axis is width and Y axis is height
    orig=img
    img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img=cv2.medianBlur(img,5)
    img=cv2.erode(img,None, iterations=2)
    img=cv2.GaussianBlur(img,(11,11),0)
    lower_g=np.array([29,86,6])
    upper_g=np.array([64,255,255])
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    ORANGE_MIN = np.array([5, 50, 50],np.uint8)
    ORANGE_MAX = np.array([15, 255, 255],np.uint8)
    #mask = cv2.inRange(img,ORANGE_MIN,ORANGE_MAX)
    mask = cv2.inRange(img,lower_g,upper_g)
    #mask = cv2.inRange(img,lower_blue,upper_blue)
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]
    img=green
    img=cv2.cvtColor(img,cv2.COLOR_HSV2RGB)
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    cimg=img
    
    circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.3,200,param1=50,param2=45,minRadius=1, maxRadius=80)
    '''if len(contours) != 0:
        #cv2.drawContours(img, contours, -1, 255, 3)
        c = max(contours, key = cv2.contourArea)
        (x,y),r = cv2.minEnclosingCircle(c)
        if(r>10.0):
            cv2.circle(img, (int(x), int(y)), int(r), (255,255,255), 2)
        return img'''
    try:
        circles[0]
    except:
        return orig
    circles=np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(orig,(i[0],i[1]),int(i[2]),(0,0,255),2)
        s="Ball detected closer to "
        s=s+position(int(i[0]),int(i[1]),h,w)+"corner"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(orig,s,(10,50), font, 0.65,(0,0,0),1,cv2.LINE_AA)
        area=3.14*int(i[2])**2
        round(area,2)
        s=" Area = "+str(area)+" square pixels"
        
        cv2.putText(orig,s,(10,80), font, 0.65,(0,0,0),1,cv2.LINE_AA)
        #cv2.circle(orig,(i[0],i[1]),2,(0,0,255),3)
    return orig


def start():
    cap=cv2.VideoCapture(0)
    while True:
        success, img=cap.read()
        img=ret_im(img)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')