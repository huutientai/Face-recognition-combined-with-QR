import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import pickle
from datetime import datetime
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials
from firebase_admin import db
from pyzbar.pyzbar import decode


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
                if faceDis < 0.6:
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


"""
def thongtin(myData):
    if myData in studentIds:
        index = studentIds.index(myData)
        id = studentIds[index]
        studentInfo = db.reference(f'Students/{id}').get()
        blob = bucket.get_blob(f'Images/{id}.png')
        array = np.frombuffer(blob.download_as_string(), np.uint8)
        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        # Kiểm tra xem khóa 'standing' có tồn tại trong studentInfo hay không

        cv2.putText(imgBackground, str(studentInfo.get('total_attendance', 'N/A')), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentInfo.get('major', 'N/A')), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        (w, h), _ = cv2.getTextSize(studentInfo.get('name', 'N/A'), cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground, str(studentInfo.get('name', 'N/A')), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

"""
# Khởi tạo VideoCapture cho camera
video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)
# url = "http://192.168.0.101:4747/video"
# video = cv2.VideoCapture(url)

# Initialize Tkinter window
root = tk.Tk()
root.title("Face Recognition App")

# Create a label to display the video feed
label = ttk.Label(root)
label.grid(row=0, column=0, columnspan=3)

# Default mode
use_qr_code = True
face_reco = False
myData = None  # Initialize myData

# Function to update the video feed
def update_video():
    global myData  # Use the global variable
    ret, frame = video.read()
    if use_qr_code == True and face_reco == False:
        myData = qrbrcode(frame)
    else:
        facerecognitionnew(myData, frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)
    label.img = frame
    label.config(image=frame)
    label.after(10, update_video)

# Function to handle button "q"
def handle_quit():
    video.release()
    root.destroy()

# Function to handle button "1"
def use_qr_code_mode():
    global use_qr_code, face_reco
    use_qr_code, face_reco = True, False

# Function to handle button "2"
def use_face_recognition_mode():
    global use_qr_code, face_reco
    use_qr_code, face_reco = False, True

# Create buttons
button_quit = ttk.Button(root, text="Quit", command=handle_quit)
button_qr_code = ttk.Button(root, text="Use QR Code", command=use_qr_code_mode)
button_face_recognition = ttk.Button(root, text="Use Face Recognition", command=use_face_recognition_mode)

# Grid layout for buttons
button_quit.grid(row=1, column=0)
button_qr_code.grid(row=1, column=1)
button_face_recognition.grid(row=1, column=2)

# Start updating video feed
update_video()

# Run Tkinter main loop
root.mainloop()