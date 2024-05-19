import pickle
from datetime import datetime

import cv2
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials
from firebase_admin import db
from pyzbar.pyzbar import decode

# Khởi tạo biến cờ để kiểm soát trạng thái bật/tắt camera cho từng camera
camera1_enabled = True
camera2_enabled = True

# Khởi tạo Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://databasefaceandscan-default-rtdb.firebaseio.com/",
    'storageBucket': "databasefaceandscan.appspot.com"
})

# Đọc danh sách encoding và studentIds từ tệp pickle
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds


# Hàm bật/tắt camera cho từng camera
# camera máy tính
def toggle_camera1():
    global camera1_enabled
    camera1_enabled = not camera1_enabled


# camera điện thoại
def toggle_camera2():
    global camera2_enabled
    camera2_enabled = not camera2_enabled


def qrbrcode(img):
    idface = None  # Giá trị mặc định nếu không có dữ liệu QR code
    for barcode in decode(img):
        print(barcode.data)
        idface = barcode.data.decode('utf-8')
        my_color = (0, 0, 255)  # Màu mặc định

        if idface in studentIds:
            my_color = (0, 255, 0)  # Đổi màu thành xanh tìm thấy myData

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, my_color, 5)
        pts2 = barcode.rect
        cv2.putText(img, idface, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, my_color, 2)

    return idface  # Trả về giá trị myData (có thể là None nếu không tìm thấy QR code)


def facerecognitionnew(myData, frame):
    matches = []

    # Kiểm tra xem có khuôn mặt trong bức ảnh không
    faceCurFrame = face_recognition.face_locations(frame)
    encodeCurFrame = face_recognition.face_encodings(frame, faceCurFrame)

    if faceCurFrame:
        if myData in studentIds:
            index = studentIds.index(myData)

            if encodeCurFrame:
                encodeKnown = [encodeListKnown[index]]
                encodeFace = encodeCurFrame[0]

                faceDis = face_recognition.face_distance(encodeKnown, encodeFace)
                if faceDis < 0.45:
                    check = 'tim thay'
                    Color = (0, 255, 0)
                    id = studentIds[index]

                    # Lấy thông tin sinh viên từ Firebase
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)
                    # Cập nhật thông tin
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    if secondsElapsed > 5:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(current_time)
                    else:
                        check = 'da diem danh'
                        Color = (0, 0, 255)
                else:
                    print("Không có trong dữ liệu")
                    check = 'khong tim thay'
                    Color = (0, 0, 255)
            else:
                print("Không tìm thấy khuôn mặt trong ảnh")
                check = 'khong tim thay'
                Color = (0, 0, 255)
        else:
            print("myData không hợp lệ")
            check = 'khong tim thay'
            Color = (0, 0, 255)

        # Vẽ đường viền xung quanh khuôn mặt
        for face_location in faceCurFrame:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), Color, 2)
            cv2.putText(frame, check, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, Color, 2)
        # Khởi tạo VideoCapture cho camera 0 (camera mặc định) và URL


video2 = cv2.VideoCapture(0)
video2.set(3, 640)
video2.set(4, 480)
# camera điện thoại
url = "http://192.168.0.101:4747/video"
video = cv2.VideoCapture(url)

while True:
    # camera máy tính
    ret2, frame2 = video2.read()
    # camera điện thoại
    ret, frame = video.read()

    if camera2_enabled and ret:
        myData = qrbrcode(frame)
        cv2.imshow("cam2", frame)  # camera điện thoại
    if camera1_enabled and ret2:
        facerecognitionnew(myData, frame2)
        cv2.imshow("cam1", frame2)  # camera máy tính

    key = cv2.waitKey(1) & 0xff
    if key == ord("q"):
        break
    elif key == ord("1"):
        # Bật/tắt camera 1 khi nhấn phím "1"
        toggle_camera1()
    elif key == ord("2"):
        # Bật/tắt camera 2 khi nhấn phím "2"
        toggle_camera2()

video.release()
video2.release()
cv2.destroyAllWindows()
