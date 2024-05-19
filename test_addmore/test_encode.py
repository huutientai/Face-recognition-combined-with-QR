import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import cv2
import face_recognition
import numpy as np
import pickle
import os

# Khởi tạo Firebase
cred = credentials.Certificate("testfacedlib.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "test-11ecb.appspot.com"
})

# Tạo một đối tượng Storage từ Firebase
bucket = storage.bucket()

# Đường dẫn đến thư mục trong Firebase Storage
folder_path = ""  # Thay đổi thành đường dẫn của thư mục bạn muốn tải

# Tạo một dictionary để lưu trữ thông tin về hình ảnh
image_dict = {}

def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img)

        # Kiểm tra xem có khuôn mặt nào được tìm thấy hay không
        if face_locations:
            # Kiểm tra lại xem có khuôn mặt nào được tìm thấy sau khi tăng kích thước
            encode = face_recognition.face_encodings(img, face_locations)[0]
            encodeList.append(encode)
        else:
            print("Không tìm thấy khuôn mặt trong ảnh!")

    return encodeList


print("encoding Started")

# Lấy danh sách blobs
blobs_iterator = bucket.list_blobs(prefix=folder_path)

# Chuyển đổi iterator thành list
blobs_list = list(blobs_iterator)

# Lặp qua danh sách blobs và thêm thông tin vào dictionary
for blob in blobs_list:
    if blob.name.endswith('.png'):
        user_id = int(blob.name.split('/')[0])

        if user_id not in image_dict:
            image_dict[user_id] = {
                'encodings': []
            }

        # Tải hình ảnh từ URL
        image_data = blob.download_as_string()
        array = np.frombuffer(image_data, np.uint8)

        # Check if img_array is not empty
        if array.size > 0:
            # Decode the image
            img = cv2.imdecode(array, cv2.IMREAD_COLOR)

            # Check if img is not empty
            if img is not None:
                # Tìm và thêm encode vào danh sách
                encodings = findEncoding([img])

                # Check if encodings is not empty
                if encodings:
                    image_dict[user_id]['encodings'].extend(encodings)
                else:
                    print("Không tìm thấy khuôn mặt trong ảnh sau khi tăng kích thước!")
            else:
                print("Failed to decode image.")
        else:
            print("Empty image array.")


print("encoding complete")
# In ra dictionary kết quả
print(image_dict)
file = open("Encode.p",'wb')
pickle.dump(image_dict,file)
file.close()
print("file saved")