import cv2
import numpy as np
import os
import face_recognition
from pyzbar.pyzbar import decode
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import pandas as pd

# Khởi tạo Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://databasefaceandscan-default-rtdb.firebaseio.com/",
    'storageBucket': "databasefaceandscan.appspot.com"
})

# Hàm xuất dữ liệu Firebase ra file Excel
def export_firebase_to_excel(excel_filename):
    try:
        # Lấy dữ liệu từ Firebase
        ref = db.reference('Students')
        students_data = ref.get()

        # Kiểm tra xem có dữ liệu hay không
        if not students_data:
            print("No data found in Firebase.")
            return

        # Tạo DataFrame từ dữ liệu Firebase với các cột mong muốn
        df = pd.DataFrame({

            'Student_ID': list(students_data.keys()),  # Thay đổi tên cột

            'name': [data['name'] if isinstance(data, dict) and 'name' in data else '' for data in students_data.values()],
            'total_attendance': [data['total_attendance'] if isinstance(data, dict) and 'total_attendance' in data else data for data in students_data.values()]
        })

        # Xuất DataFrame ra file Excel
        df.to_excel(excel_filename, index_label='stt')  # Thay đổi tên cột

        print(f"Data exported to {excel_filename} successfully!")

    except Exception as e:
        print("Error exporting data to Excel:", str(e))

# Gọi hàm để xuất dữ liệu
export_firebase_to_excel("diemdanh_3.xlsx")
