#人臉註冊部分#
# input 照片_編號 10張照片
# output 把這10張照片變成 json 並新增到 face_info 的 json
#再把新註冊的使用者照片跟資料夾刪掉
import sys,os,dlib,glob
import numpy as np
from skimage import io
import imutils
import cv2
import json
import os
import shutil
import time
#新增放新註冊使用者圖片的資料夾
#os.mkdir("./new_user")



from face_detecton.face_vector import picture_to_vector_json


def get_ten_pics_and_features(video,username):
    cap = cv2.VideoCapture(video)  # play video file

    FPS = cap.get(cv2.CAP_PROP_FPS)  # Frame Per Second
    F_Count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # frame count
    print(f'FPS : {FPS:.2f} ms, Frame_Count : {F_Count}')
    count = 0
    count_limit = 10  # 截取圖片張數
    
    
    b = 0 # 設定每隔多久要抓一次照片
    timeF = 10
    while cap.isOpened():
        
        ret, frame = cap.read()
        
        if not ret: break
        if(b%timeF == 0):
            c = cv2.waitKey(30)  # 25 ms per frame     1/FPS

            img_path='./new_user/{}_{}.jpg'.format(username,count)
            cv2.imencode('.jpg', frame)[1].tofile(img_path)
            #cv2.imwrite('中文{}.jpg'.format(count), frame)  # save frame as JPEG file
            print('save image : {}_{}.jpg'.format(username,count))
            count += 1
        b = b + 1
        if (not ret or c == 27) or (count > count_limit):
            break
           
    cap.release()
