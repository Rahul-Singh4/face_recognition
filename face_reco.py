import cv2
import face_recognition
import os
import numpy as np
from datetime import  datetime
import mysql.connector as mysql
directory = r'C:/Users/Rahul0004/Desktop/Project/Dataset/Images'#taking the dataset
os.chdir(directory) 
images=[]
clsName=[]
mylist=os.listdir(directory)

for c1 in mylist:
    curImg=cv2.imread(f'{directory}/{c1}')#read the images
    images.append(curImg)#Adding to the images array
    clsName.append(os.path.splitext(c1)[0])#Removing the extension of image and adding in clsName 1018556 png

def findEncoding(images):
    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)#Converting image RGB
        encode=face_recognition.face_encodings(img)[0]#Given an image, return the 128-dimension face encoding for each face in the image.
        encodelist.append(encode)#Appending the encode in encodelist
    return encodelist

def markAttend(ID):
    name=""
    branch=""
    with open('..\..\Attendence.csv','r+') as f:
        myData=f.readlines()
        IDList=[]
        for line in myData:
            entry=line.split(',')
            IDList.append(entry[0])
        if ID not in IDList:
            con=mysql.connect(host="localhost",user="root",password="User@1234",database="Regform")
            cursor=con.cursor()
            cursor.execute("select * from Reg")
            results=cursor.fetchall()
            for i in results:
                if ID==i[1]:
                    name=i[0]
                    branch=i[2]
                    break

            now=datetime.now()
            dstring=now.strftime("%H:%M:%S")
            f.writelines(f'\n{ID},{name},{dstring}')

encodeKnown=findEncoding(images)#Encoding of all known faces
cap=cv2.VideoCapture(0)#To capture the video
while True:
    value,img=cap.read()#returns a bool (True/False). If img is read correctly, it will be True.
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)#Reducing the size (1/4th of original size)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)#converting into RGB
    faceCurFrame=face_recognition.face_locations(imgS)#finding the face location
    encodesCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

    for encodeFace,Faceloc in zip(encodesCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeKnown,encodeFace)#comparing faces from the known faces
        faceDis=face_recognition.face_distance(encodeKnown,encodeFace)#The distance tells you how similar the faces are
        matchIndex=np.argmin(faceDis)#It will give the min value index
        if matches[matchIndex]:
            name=""
            ID=clsName[matchIndex]
            con=mysql.connect(host="localhost",user="root",password="User@1234",database="Regform")
            cursor=con.cursor()
            cursor.execute("select * from Reg")
            results=cursor.fetchall()
            for i in results:
                if ID==i[1]:
                    name=i[0]
                    break
            
            y1,x2,y2,x1=Faceloc#face location
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4#convert into original image
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,200),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,200),cv2.FILLED)
            cv2.putText(img,name,(x1+10,y2-12),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)
            
            markAttend(ID)
            cv2.putText(img,"Attendance Marked",(x1+12,y1-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,124,0),2,cv2.LINE_AA)

    cv2.imshow('webcam',img)
    if cv2.waitKey(1) &0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


