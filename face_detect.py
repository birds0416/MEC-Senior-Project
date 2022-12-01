import matplotlib.pyplot as plt
import cv2
import os
import glob

def face_detector(path, folderName, unorganized):

    try:
        os.mkdir(folderName)
    except OSError:
        print("Creation of the directory %s failed" % folderName)
    else:
        print("Successfully created the directory %s " % folderName)

    try:
        os.mkdir(unorganized)
    except OSError:
        print("Creation of the directory %s failed" % unorganized)
    else:
        print("Successfully created the directory %s " % unorganized)

    cascade_file = "cascade/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_file)

    files = glob.glob(path)
    imgsraw = []
    for i in files:
        a = i.split("/")
        b = a[len(a) - 1].split("\\")
        imgsraw.append(b[1])
    imgs = []
    for i in imgsraw:
        i = "photos/" + i
        imgs.append(i)

    for i in range(0, len(imgs)):
        img = cv2.imread(imgs[i])
        temp = cv2.imread(imgs[i])
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 얼굴 인식하기
        face_list = cascade.detectMultiScale(img_gray, minSize=(150, 150))
        # 결과 확인하기
        if len(face_list) == 0:
            print("Failure")
            name = unorganized + str(i) + ".jpg"
            cv2.imwrite(name, img)
        # 인식한 부분 표시하기
        else:
            for (x, y, w, h) in face_list:
                yellow = (0, 255, 255)
                cv2.rectangle(img, (x, y), (x + w, y + h), yellow, thickness=20)
                print("Success")

            name = folderName + str(i) + ".jpg"
            cv2.imwrite(name, temp)
            plt.imshow(cv2.cvtColor(temp, cv2.COLOR_BGR2RGB))
            plt.show()

# path = input("Path: ")
# path += "/*.jpg"
# folderName = input("Folder name: ")wwwwwwwww
# unorganized = folderName + unorganized + "/"

path = "C:/Users/birds/Google Drive/코딩/machine_learning/photos/*.jpg"
folderName = "C:/Users/birds/Desktop/new_photos/"
unorganized = "C:/Users/birds/Desktop/new_photos/not_human/"

face_detector(path, folderName, unorganized)

