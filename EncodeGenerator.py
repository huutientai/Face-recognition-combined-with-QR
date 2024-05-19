import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import numpy as np
import cv2
import face_recognition
import pickle
import os

# Khởi tạo Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "databasefaceandscan.appspot.com"
})

# Tạo một đối tượng Storage từ Firebase
bucket = storage.bucket()

# Đường dẫn đến thư mục trong Firebase Storage
folder_path = "Images"  # Thay đổi thành đường dẫn của thư mục bạn muốn tải

# Liệt kê tất cả các đối tượng trong thư mục
blobs = bucket.list_blobs(prefix=folder_path)


# Khởi tạo danh sách để lưu trữ hình ảnh
imglist = []

studentIds = []
# Lặp qua từng đối tượng (tệp tin) và tải chúng nếu có đuôi .png
for blob in blobs:
    if blob.name.lower().endswith('.png'):
        # Tải hình ảnh từ Firebase Storage
        image_data = blob.download_as_string()

        # Chuyển dữ liệu thành mảng numpy
        array = np.frombuffer(image_data, np.uint8)

        # Đọc hình ảnh bằng OpenCV
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)

        # Thêm hình ảnh vào danh sách
        imglist.append(image)

        # Lấy tên hình ảnh và thêm vào danh sách studentIds
        student_id = os.path.splitext(blob.name)[0].split("/")[-1]
        studentIds.append(student_id)

# Bây giờ, biến imglist sẽ chứa danh sách các hình ảnh và biến studentIds sẽ chứa danh sách các tên hình ảnh.

print(studentIds)

def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList



print("encoding Started")
# gia tri diem
encodeListKnown = findEncoding(imglist)

# print(encodeListKnown)
# dua 2 cai vao
encodeListKnownWithIds = [encodeListKnown,studentIds]
print("encoding complete")
print(encodeListKnownWithIds)

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("file saved")

