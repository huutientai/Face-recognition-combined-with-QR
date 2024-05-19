import pickle
from datetime import datetime
import pyttsx3
import cv2
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials
from firebase_admin import db
from pyzbar.pyzbar import decode

cred = credentials.Certificate("testfacedlib.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://test-11ecb-default-rtdb.firebaseio.com/",
    'storageBucket': "test-11ecb.appspot.com"
})
# Read encoding and studentIds from the pickle file
with open('Encode.p', 'rb') as file:
    # Sử dụng pickle để load dữ liệu từ file
    encodeData = pickle.load(file)

studentIds = [int(k) for k in encodeData.keys() if k != 'encodeListKnown']
# Set initial mode to QR code

# qrbrcode_Check = True
# face_Check = False
# myData = None

def text_to_speech(text):
    # Khởi tạo đối tượng pyttsx3
    engine = pyttsx3.init()

    # Đặt các thuộc tính tùy chọn nếu cần thiết (ví dụ: tốc độ)
    engine.setProperty('rate', 150)  # Tốc độ của giọng nói

    # Xuất giọng nói từ văn bản
    engine.say(text)

    # Đợi cho đến khi giọng nói hoàn thành
    engine.runAndWait()

# Function to process QR code
def qrbrcode(img):
    global qrbrcode_Check, face_Check
    idface = None
    my_color = (0, 0, 255)  # Default color

    for barcode in decode(img):
        print(barcode.data)
        idface = int(barcode.data.decode('utf-8'))

        if idface in studentIds:
            my_color = (0, 255, 0)  # Change color to green if myData is found
            qrbrcode_Check = False
            face_Check = True  # Set face_Check to True

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, my_color, 5)
        pts2 = barcode.rect
        cv2.putText(img, str(idface), (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, my_color, 2)

    return idface

# Function to process face recognition
# Function to process face recognition
def facerecognitionnew(myData, frame):
    global qrbrcode_Check, face_Check
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



    faceCurFrame = face_recognition.face_locations(frame)
    encodeCurFrame = face_recognition.face_encodings(frame, faceCurFrame)

    # Initialize Color with a default value
    Color = (0, 0, 255)
    check = ''  # Initialize check with an empty string

    if faceCurFrame:
        if myData in studentIds:
            index = int(studentIds.index(myData))

            if encodeCurFrame:
                encodeKnown = encodeData[myData]


                encodeFace = encodeCurFrame[0]

                # faceDis = face_recognition.face_distance(encodeKnown, encodeFace)
                # need fix
                facemark = face_recognition.compare_faces([encodeKnown],encodeFace)

                if sum(facemark) >= 1:
                    check = 'tim thay'
                    Color = (0, 255, 0)
                    id = studentIds[index]

                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)

                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    if secondsElapsed > 5:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(current_time)
                        qrbrcode_Check = True  # Set qrbrcode_Check to True
                        face_Check = False
                        text_to_speech("Took attendance")

                        # Chờ 1 giây
                        cv2.waitKey(1000)
                    else:
                        check = 'da diem danh'
                        Color = (0, 0, 255)

    for face_location in faceCurFrame:
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), Color, 2)
        cv2.putText(frame, check, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, Color, 2)

qrbrcode_Check = True
face_Check = False
myData = None

video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)

while True:
    ret, frame = video.read()

    # Display frame from the camera and process based on the current mode
    if qrbrcode_Check:
        myData = qrbrcode(frame)
        print(myData)
        if myData is not None:
            cv2.waitKey(3000)
            start_time = datetime.now()

    elif face_Check:
        print("bat dau khuon mat")
        print(f"myData: {myData}")
        print(f"frame shape: {frame.shape}")
        facerecognitionnew(myData, frame)
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time > 4:
            qrbrcode_Check = True
            face_Check = False
            myData = None


    # Display the camera feed
    cv2.imshow("Camera", frame)

    # Check for key press to exit
    key = cv2.waitKey(1) & 0xff
    if key == ord("q"):
        break

# Release the camera and close the window
video.release()
cv2.destroyAllWindows()