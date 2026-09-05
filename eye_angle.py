import math

import cv2
import os
import numpy as np


def getEyeAngle(image):
    cascade_dir = cv2.data.haarcascades
    face_casc_xmlpath = os.path.join(cascade_dir,"haarcascade_eye.xml")
    if os.path.exists(face_casc_xmlpath):
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        eye_cascade = cv2.CascadeClassifier(face_casc_xmlpath)
        eye = eye_cascade.detectMultiScale(gray_image,scaleFactor=1.1,minNeighbors=5,minSize=(20,20))
        print("eye",eye)
        sore = sorted(eye,key=lambda x:x[3],reverse=True)
        print("sore",sore)
        if len(eye):
            sortedarr = []
            for index in range(2):
                sortedarr.append(eye[index].tolist()) 
            sortedarr.sort(reverse=False)
            print("sortedarr",sortedarr)
            #x,y,h,w ,, [[1377, 1731, 241, 241], [1901, 1704, 301, 301]]
            #get angle of eyes

            # 1 get left eye center point
            leCenterErr = sore[0][-1]/2
            leftEyeCenter = [sore[0][0]+leCenterErr, sore[0][1]+leCenterErr]
            cv2.circle(image,(int(leftEyeCenter[0]),int(leftEyeCenter[1])), 1, (0,255,255), 12)
            # 2 get left eye center point
            reCenterErr = sore[1][-1]/2
            rightEyeCenter = [sore[1][0]+reCenterErr, sore[1][1]+reCenterErr]
            cv2.circle(image,(int(rightEyeCenter[0]),int(rightEyeCenter[1])), 1, (0,255,255), 12)

            # 3 get center of both eyes 
            beCenterX = (leftEyeCenter[0]+rightEyeCenter[0])//2
            beCenterY = (leftEyeCenter[-1]+rightEyeCenter[-1])//2
            print(beCenterY)
            errY = (rightEyeCenter[-1]-beCenterY)
            cv2.circle(image,(int(beCenterX),int(beCenterY)),1,(0,255,255),12)
            print(errY,leftEyeCenter,rightEyeCenter)
            
            angle = math.degrees(math.atan(errY/(beCenterX-rightEyeCenter[0])))
            print(round(angle))
            
            for i in range(2):
                x,y,w,h = sore[i]
                cv2.rectangle(image,(x,y), (x+w, y+h), (0,255,0),4)
                # cv2.imwrite("output.jpg",image)

            return image,angle
    print("not exists")


# from PIL import Image

# image = Image.open("image2.webp")
# rotateImage = image.rotate(40)
# rotateImage.save("rotated.jpg")