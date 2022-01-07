### 將人臉圖片資料庫的每個照片算出128維人臉特徵向量後，存成 { 人名 : [128維特徵向量] } 的json檔案 ###

import sys, os, dlib, glob
import numpy as np
from skimage import io
import imutils
import cv2
import json
import os

def picture_to_vector_json():
    # 人臉圖片資料夾名稱
    faces_data_path = "./new_user"
    # 開啟影片檔案
    #cap = cv2.VideoCapture(0)
    # 載入人臉檢測器
    detector = dlib.get_frontal_face_detector()
    # 人臉68特徵點模型的路徑及檢測器
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    # 載入人臉辨識模型及檢測器
    face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
    # 人臉描述子list
    descriptors = []
    # 候選人臉名稱list
    candidate = []
    # 人臉跟128維度向量的dict
    name_vector = {}

    for file in glob.glob(os.path.join(faces_data_path, "*.jpg")):
        base = os.path.basename(file)
        # 讀取人臉圖片資料夾的每張圖片
        # os.path.join())用於拼接檔案路徑
        # os.path,splitext()分離檔名及副檔名
        face_name = os.path.splitext(base)[0]
        candidate.append(face_name)
        img = io.imread(file)

        # 人臉偵測
        dets = detector(img, 1)

        for k, d in enumerate(dets):
            # 68特徵點偵測
            shape = shape_predictor(img, d)

            # 128維特徵向量描述子
            face_descriptor = face_rec_model.compute_face_descriptor(img, shape)

            # 轉換 numpy array 格式
            v = np.array(face_descriptor)
            descriptors.append(v)

            # 把人名跟向量打包成name_vector這個dict
            face_descriptor_list = list(face_descriptor)

            name_vector[face_name] = face_descriptor_list
            # 將dict轉成json
            name_vector_json = json.dumps(name_vector,ensure_ascii=False)
            print(name_vector_json)

    # 完成處理後匯出檔案
    with open("./user_face_info.json", "w", encoding='utf-8') as f:
        json.dump(name_vector_json, f,ensure_ascii=False)
    print("打包完成")