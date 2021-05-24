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

def perc_change(x1,y1,x2,y2):
    p1=int(((x1-x2)/x1)*100)
    p2=int(((x1-x2)/x1)*100)
    if(p1<=12 and p2<=12):
        return True
    else:
        return False

def find_common(circles, x, y ):
    x,y=int(x),int(y)
    for i in circles[0,:]:
        i[0],i[1]=int(i[0]),int(i[1])
        if(perc_change(x,y,i[0],i[1])):
            return True
        else:
            print(x,y,i[0],i[1])
    return False


def ret_im(img):
    h,w,c=img.shape #X axis is width and Y axis is height
    orig=img
    img=cv2.GaussianBlur(img,(7,7),0)
    grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_g=np.array([37,25,25])
    upper_g=np.array([85,255,255])
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    ORANGE_MIN = np.array([5, 50, 50],np.uint8)
    ORANGE_MAX = np.array([15, 255, 255],np.uint8)
    #mask = cv2.inRange(img,ORANGE_MIN,ORANGE_MAX)
    mask = cv2.inRange(img,lower_g,upper_g)
    #mask = cv2.inRange(img,lower_blue,upper_blue)
    img = cv2.bitwise_and(img,img , mask=mask)
    #return img
    img=cv2.cvtColor(img,cv2.COLOR_HSV2RGB)
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    cimg=img
    
    mask=cv2.erode(img,None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None
    circles=cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT,1,200,param1=60,param2=40,minRadius=0, maxRadius=0)
    #circles=np.uint16(np.around(circles))
    if len(contours) != 0:
        c = max(contours, key = cv2.contourArea)
        (x,y),r = cv2.minEnclosingCircle(c)
        try:
            circles[0]
        except:
            return orig
        if(r>10.0 and find_common(circles,x,y)):
            cv2.circle(orig, (int(x), int(y)), int(r), (255,255,255), 2)
            s="Ball detected closer to "
            s=s+position(int(x),int(y),h,w)+" corner"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(orig,s,(10,50), font, 0.65,(0,0,0),1,cv2.LINE_AA)
            area=3.14*int(r)**2
            area=round(area,2)
            s=" Area = "+str(area)+" square pixels"
            
            cv2.putText(orig,s,(10,80), font, 0.65,(0,0,0),1,cv2.LINE_AA)
        return orig
    try:
        circles[0]
    except:
        return orig
    '''
    for i in circles[0,:]:
        cv2.circle(orig,(i[0],i[1]),int(i[2]),(0,0,255),2)
        s="Ball detected closer to "
        s=s+position(int(i[0]),int(i[1]),h,w)+" corner"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(orig,s,(10,50), font, 0.65,(0,0,0),1,cv2.LINE_AA)
        area=3.14*int(i[2])**2
        round(area,2)
        s=" Area = "+str(area)+" square pixels"
        
        cv2.putText(orig,s,(10,80), font, 0.65,(0,0,0),1,cv2.LINE_AA)
        #cv2.circle(orig,(i[0],i[1]),2,(0,0,255),3)
    return orig
'''

def start():
    cap=cv2.VideoCapture(0)
    while True:
        success, img=cap.read()
        img=ret_im(img)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')