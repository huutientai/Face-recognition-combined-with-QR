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

class FaceRecognitionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Initialize VideoCapture for the camera
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 640)
        self.video.set(4, 480)

        # Create a label to display the video feed
        self.label = ttk.Label(window)
        self.label.grid(row=0, column=0, columnspan=3)

        # Default mode
        self.use_qr_code = True
        self.face_reco = False
        self.my_data = None  # Initialize myData

        # Create buttons
        self.button_quit = ttk.Button(window, text="Quit", command=self.handle_quit)
        self.button_qr_code = ttk.Button(window, text="Use QR Code", command=self.use_qr_code_mode)
        self.button_face_recognition = ttk.Button(window, text="Use Face Recognition", command=self.use_face_recognition_mode)

        # Grid layout for buttons
        self.button_quit.grid(row=1, column=0)
        self.button_qr_code.grid(row=1, column=1)
        self.button_face_recognition.grid(row=1, column=2)

        # Start updating video feed
        self.update_video()

    # Function to update the video feed
    def update_video(self):
        ret, frame = self.video.read()
        if self.use_qr_code:
            self.my_data = self.qr_code(frame)
        else:
            self.facerecognitionnew(self.my_data, frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.label.img = frame
        self.label.config(image=frame)
        self.label.after(10, self.update_video)

    # Function to handle button "Quit"
    def handle_quit(self):
        self.video.release()
        self.window.destroy()

    # Function to handle button "Use QR Code"
    def use_qr_code_mode(self):
        self.use_qr_code, self.face_reco = True, False

    # Function to handle button "Use Face Recognition"
    def use_face_recognition_mode(self):
        self.use_qr_code, self.face_reco = False, True

    # Function to decode QR code
    def update_video(self):
        ret, frame = self.video.read()
        if self.use_qr_code:
            self.my_data = self.qr_code(frame)
        else:
            self.facerecognitionnew(self.my_data, frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.label.img = frame
        self.label.config(image=frame)
        self.label.after(10, self.update_video)

    def facerecognitionnew(self, myData, frame):
        matches = []

        # Kiểm tra xem có khuôn mặt trong bức ảnh không
        face_cur_frame = face_recognition.face_locations(frame)
        encode_cur_frame = face_recognition.face_encodings(frame, face_cur_frame)

        if face_cur_frame:
            for face_location in face_cur_frame:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            if my_data in studentIds:
                index = studentIds.index(my_data)

                if encode_cur_frame:
                    encode_known = [encodeListKnown[index]]
                    encode_face = encode_cur_frame[0]

                    face_dis = face_recognition.face_distance(encode_known, encode_face)
                    if face_dis < 0.6:
                        check = 'tim thay'
                        color = (0, 255, 0)
                        id = studentIds[index]

                        # Lấy thông tin sinh viên từ Firebase
                        student_info = db.reference(f'Students/{id}').get()
                        print(student_info)
                        # Cập nhật thông tin
                        datetime_object = datetime.strptime(student_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                        seconds_elapsed = (datetime.now() - datetime_object).total_seconds()
                        if seconds_elapsed > 30:
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ref = db.reference(f'Students/{id}')
                            student_info['total_attendance'] += 1
                            ref.child('total_attendance').set(student_info['total_attendance'])
                            ref.child('last_attendance_time').set(current_time)
                        else:
                            check = 'da diem danh'
                            color = (0, 0, 255)
                    else:
                        print("Not found in the data")
                        check = 'khong tim thay'
                        color = (0, 0, 255)
                else:
                    print("No faces found in the image")
                    check = 'khong tim thay'
                    color = (0, 0, 255)
            else:
                print("my_data is not valid")
                check = 'khong tim thay'
                color = (0, 0, 255)

            # Vẽ đường viền xung quanh khuôn mặt và hiển thị thông tin
            for face_location in face_cur_frame:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, check, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    def qr_code(self, img):
        idface = None
        for barcode in decode(img):
            idface = barcode.data.decode('utf-8')
            my_color = (0, 0, 255)

            if idface in studentIds:
                my_color = (0, 255, 0)

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, my_color, 5)
            pts2 = barcode.rect
            cv2.putText(img, idface, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, my_color, 2)

        return idface



update()
window.mainloop()
