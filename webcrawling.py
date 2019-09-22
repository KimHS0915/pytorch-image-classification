from google_images_download import google_images_download 
import os
import cv2
import glob

def imagedownloader(keywords, output_directory, limit=50):

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords":keywords,"limit":limit,"format":'jpg', "prefix":False, "type":'face', 'no_directory':True, 'output_directory':output_directory}

    response.download(arguments)

def facecrop_directory(input_path, output_path, resize_dim=(32,32)):
    number = 0
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
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
            cv2.imwrite(f'{output_path}face{str(number)}.jpg', resized)

"""
ex)
imagedownloader('man', 'd:/data/pic/', 100)
facecrop_directory('d:/data/pic/', 'd:/data/faces/', (128,128))
"""
