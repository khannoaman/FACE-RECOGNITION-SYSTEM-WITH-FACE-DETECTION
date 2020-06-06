import cv2
import mysql.connector
import datetime
import re
import sys
import os

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
try:
    conn=mysql.connector.connect(host="localhost",user="root",passwd="8800288198",database="facerecognition-data")
    mycursor=conn.cursor()
except Exception as e:
    print(e)
    sys.exit()

def face_extractor(img):

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces ==():
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face

inp=int(input("What do you want to do?(1-3)\n1-Register for your Face Recognition(Create Dataset).\n2-Already Registered but want to add more Images to your dataset.\n3-Delete your dataset.\n->"))
imageCount = 0
count = 0
if inp==1:
    d=datetime.datetime.now()
    id=re.findall(r'\d{1}:\d{2}\.',str(d))
    id=re.sub(r'(-|:|\.| )',"",id[0])
    name=input("\nPlease Enter your name.\n->")
    print("\nYour id is: {}\n".format(id))
    imageCount=200

    #Storing data into database
    try:
        mycursor.execute("INSERT INTO `data` (`ID`, `Name`, `ImageCount`) VALUES ({}, '{}', {});".format(int(id),name,imageCount))
    except Exception as e:
        print(e)
        sys.exit()

elif inp==2:
    id=input("\nPlease Enter your Id\n->")

    try:
        mycursor.execute("select ImageCount from data where id={}".format(int(id)))
        if mycursor.fetchone()!=None:
            mycursor.execute("select ImageCount from data where id={}".format(int(id)))
            n=mycursor.fetchone()[0]
            count=n
            imageCount=n+50
            mycursor.execute("UPDATE `data` SET `ImageCount` = {} WHERE (`ID` = {});".format(imageCount,int(id)))
        else:
            print("\nWrong ID.\n")
            sys.exit()
    except Exception as e:
        print(e)
        sys.exit()

elif inp==3:
    id = input("\nPlease Enter your Id\n->")
    try:
        mycursor.execute("select * from data where id={}".format(int(id)))
        if mycursor.fetchone() != None:
            mycursor.execute("DELETE FROM `data` WHERE (`ID` = {});".format(int(id)))
            path="D:/Python Projects/Face Recognition/Dataset/"
            l=os.listdir(path)
            l=[i for i in l if "user."+id in i]
            for i in l:
                if os.path.exists(path+i):
                    os.remove(path+i)
            conn.commit()
            print("\nYour Details are deleted.\n")
            sys.exit()
        else:
            print("\nWrong ID.\n")
            sys.exit()
    except Exception as e:
        print(e)

print("\nReady for Colleting Samples!!!\n")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count+=1
        face = cv2.resize(face_extractor(frame),(200,200))


        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        file_name_path = 'D:/Python Projects/Face Recognition/Dataset/user.'+str(id)+"."+str(count)+'.jpg'
        cv2.imwrite(file_name_path,face)

        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('SAMPLES',face)
    else:
        cv2.imshow('SAMPLES', frame)
        print("Face not Found")
        pass

    if cv2.waitKey(1)==13 or count==imageCount:
        conn.commit()
        break

cap.release()
cv2.destroyAllWindows()
print('\nColleting Samples Completed!!!\n')


