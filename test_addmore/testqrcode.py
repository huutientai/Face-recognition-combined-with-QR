import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pickle

# Mở file để đọc
with open('Encode.p', 'rb') as file:
    # Sử dụng pickle để load dữ liệu từ file
    encodeData = pickle.load(file)

studenit = [int(k) for k in encodeData.keys() if k != 'encodeListKnown']

# Key bạn muốn lấy giá trị
# Key bạn muốn lấy giá trị
desired_key = '31'

try:
    # Lấy giá trị cho key cụ thể từ encodeData
    value_for_desired_key = encodeData[desired_key]
    # print(f'Giá trị cho key "{desired_key}" là: {value_for_desired_key}')
    print(f'Giá trị cho key  là: {value_for_desired_key}')
except KeyError:
    # print(f'Key "{desired_key}" không tồn tại trong encodeData.')
    print(f'Key  không tồn tại trong encodeData.')





# url = "http://192.168.0.101:4747/video"
# cap = cv2.VideoCapture(url)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:

    success, img = cap.read()
    for barcode in decode(img):
        print(barcode.data)
        myData = barcode.data.decode('utf-8')
        # print(myData)
        myData = int(myData)
        studenit = [int(k) for k in encodeData.keys() if k != 'encodeListKnown']


        if myData in studenit:
            myOutput = 'Authorized'
            myColor = (0,255,0)
        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)

        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,myColor,5)
        pts2 = barcode.rect
        cv2.putText(img,str(myData),(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,myColor,2)


    cv2.imshow('Result',img)
    cv2.waitKey(1)