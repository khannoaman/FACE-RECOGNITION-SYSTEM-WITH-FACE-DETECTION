import cv2
import numpy as np
import webbrowser
from os import listdir
from os.path import isfile, join,split

data_path = 'D:/MINOR PROJ2/Dataset/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]



Training_Data, Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype="uint8"))
    Labels.append(split(image_path)[1].split(".")[1])

Labels = np.asarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()

model.train(np.asarray(Training_Data), np.asarray(Labels))

print("Model Training Complete!!!!!")

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        return img,[]

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        cv2.rectangle(img, (x, y-50), (x + w, y -10), (0, 255, 255), 3)
        cv2.rectangle(img, (x, y - 50), (x + w, y - 10), (0,255,255), -1)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))


    return img,roi

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()

    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        id,result = model.predict(face)
        print(result)
        print(id)

        confidence = int(100 * (1 - (result) / 300))

        if id==1 and result<55:
            display_string = str(confidence)+'% CONFIDENCE IT IS NOAMAAN'


        elif id==2 and result<55:
            display_string = str(confidence) + '% CONFIDENCE IT IS AYMAN'
        elif id == 3 and result < 55:
            display_string = str(confidence) + '% CONFIDENCE IT IS VIRAT'
        elif id==4 and result<55:
            display_string = str(confidence) + '% CONFIDENCE IT IS CHANDUL'
        else:
            display_string = "     USER NOT MATCHED"
        cv2.rectangle(image, (0, 0), ( 640, 60), (224, 224, 224), -1)
        cv2.putText(image,display_string,(60,40), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)



        if confidence > 75:
            cv2.rectangle(image, (0, 420), (640, 480), (224, 224, 224), -1)
            cv2.putText(image, "UNLOCKED", (250, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 106, 8), 2)
            cv2.imshow('Face Cropper', image)
            cv2.waitKey(1000)
            webbrowser.open("https://www.google.co.in/",new=2)

            break

        else:
            cv2.rectangle(image, (0, 420), (640, 480), (224, 224, 224), -1)
            cv2.putText(image, "LOCKED", (250, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Cropper', image)


    except:
        cv2.rectangle(image, (0, 0), (640, 60), (224, 224, 224), -1)
        cv2.rectangle(image, (0, 420), (640, 480), (224, 224, 224), -1)
        cv2.putText(image, "FACE NOT FOUND", (185, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Face Cropper', image)
        pass

    if cv2.waitKey(1)==13  :
        break


cap.release()
cv2.destroyAllWindows()