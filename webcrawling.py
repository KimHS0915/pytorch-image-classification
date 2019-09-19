from google_images_download import google_images_download 
import os
import cv2
import glob

def imagedownloader(keywords, limit=100):

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords":keywords,"limit":limit,"format":'jpg', "prefix":False, "type":'face', 'no_directory':True}

    paths = response.download(arguments)
    print(paths)

def rename(path, name=''):
    number = 0
    for i in os.listdir(path):
        number += 1
        os.rename(f'{path}{i}', f'{path}{name}{number}.jpg')

def facecrop_directory(input_path, output_path, resize_dim=(32,32)):
    number = 0
    for i in glob.glob(input_path+'*'):
        number += 1
        image = cv2.imread(i)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #https://github.com/opencv/opencv/tree/master/data/haarcascades

        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
            roi = image[y:y + h, x:x + w]
            resized = cv2.resize(roi, resize_dim)
            cv2.imwrite(f'{output_path}{str(number)}.jpg', resized)
           
