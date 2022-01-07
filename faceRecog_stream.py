import sys,os,dlib,glob
import numpy as np
from skimage import io
from PIL import Image,ImageFont,ImageDraw
import imutils
import cv2

def face_detection_and_recognition():
    #設定人臉特徵距離筏值 0.4:嚴格 0.5:寬鬆
    setting_distance = 0.45

    #人臉圖片資料夾名稱
    faces_data_path = "face_detecton/new_user"
    # 開啟影片檔案
    cap = cv2.VideoCapture(0)
    #載入人臉檢測器
    detector = dlib.get_frontal_face_detector()
    #人臉68特徵點模型的路徑及檢測器
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    #載入人臉辨識模型及檢測器
    face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
    #人臉描述子list
    descriptors = []
    #候選人臉名稱list
    candidate = []

    for file in glob.glob(os.path.join(faces_data_path,"*.jpg")):
        base = os.path.basename(file)
        #讀取人臉圖片資料夾的每張圖片
        #os.path.join())用於拼接檔案路徑
        #os.path,splitext()分離檔名及副檔名

        candidate.append(os.path.splitext(base)[0])
        img = io.imread(file)

        #人臉偵測
        dets = detector(img,1)

        for k,d in enumerate(dets):
            #68特徵點偵測
            shape = shape_predictor(img,d)

            #128維特徵向量描述子
            face_descriptor = face_rec_model.compute_face_descriptor(img,shape)

            #轉換 numpy array 格式
            v = np.array(face_descriptor)
            descriptors.append(v)


    #對要辨識的目標圖片作相同處理
    #讀取照片
    while(cap.isOpened()):
        ret, frame = cap.read()
        dets = detector(frame, 1)

        distance = []

        for k,d in enumerate(dets):
            #68特徵點偵測
            shape = shape_predictor(frame,d)

            #128維特徵向量描述子
            face_descriptor = face_rec_model.compute_face_descriptor(frame,shape)

            #轉換 numpy array 格式
            d_test = np.array(face_descriptor)

            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()
            #以方框框出人臉
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),4,cv2.LINE_AA)

            #計算歐式距離，線性運算函式
            for i in descriptors:
                dist_ = np.linalg.norm(i - d_test)
                distance.append(dist_)

        #利用 zip函數將元素打包成一個元組
        #並存入dict(候選圖片,距離)
        candidate_distance_dict = dict(zip(candidate,distance))


        #接著將候選圖片及人名進行排序
        candidate_distance_dict_sorted = sorted(candidate_distance_dict.items(), key = lambda d:d[1]) #[i][0]=人名 [i][1]=距離，第一個維度是代表第 i 張人臉圖片
        pic_fit = False #尚未有符合人臉圖片庫的人臉 pic_fit設為False，若有符合則為True
        for i in range(len(candidate_distance_dict_sorted)):
            pic_distance = candidate_distance_dict_sorted[i][1]
            #print(pic_distance)
            if pic_distance < setting_distance: # 當圖片的人臉特徵距離 < 所設定的筏值，代表找到符合人臉圖片庫內的人臉
                pic_fit = True
        if pic_fit == True: # 找到符合的人臉
            try:
                result = candidate_distance_dict_sorted[0][0] #取出最短距離維辨識出的對象 #不知道為什麼會 index out of range
            except IndexError:
                pass



            #print(result1)result1（改成只輸出人名）result split的結果
            result1='用户：{}'.format(result.split('_')[0])
            print(result1)
            # cv2讀取影片
            cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pilimg = Image.fromarray(cv2img)

            # PIL圖片上輸出中文
            draw = ImageDraw.Draw(pilimg)
            font = ImageFont.truetype("SimHei.ttf", 30, encoding='utf-8')
            draw.text((x1, y1-25),result1, (255, 0, 0), font=font)

            # PIL轉cv2
            frame = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
            #在方框旁邊標上人名
            # cv2.putText(frame,result1,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
            frame = imutils.resize(frame,width = 500)
        else: # pic_fit == False
                unknown_result = "Unknown"
                try: #排除抓不到人臉會出現的Error
                    cv2.putText(frame,unknown_result,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                except NameError:
                    pass
                frame = imutils.resize(frame,width = 500)
                #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # 顯示結果
        cv2.imshow("outcome",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


face_detection_and_recognition()