from datetime import datetime
import firebase_admin
from PyQt5.QtWidgets import QLabel, QFileDialog
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
import sys


# Khởi tạo Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://databasefaceandscan-default-rtdb.firebaseio.com/",
    'storageBucket': "databasefaceandscan.appspot.com"
})

bucket = storage.bucket()

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_add_Data(object):
    def setupUi(self, add_Data):
        add_Data.setObjectName("add_Data")
        add_Data.resize(1085, 646)
        self.label = QtWidgets.QLabel(add_Data)
        self.label.setGeometry(QtCore.QRect(160, 105, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(add_Data)
        self.label_2.setGeometry(QtCore.QRect(160, 160, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setLineWidth(1)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(add_Data)
        self.label_3.setGeometry(QtCore.QRect(160, 200, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setLineWidth(1)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(add_Data)
        self.label_4.setGeometry(QtCore.QRect(160, 255, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setLineWidth(1)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(add_Data)
        self.label_7.setGeometry(QtCore.QRect(160, 105, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_7.setFont(font)
        self.label_7.setLineWidth(1)
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(add_Data)
        self.label_9.setGeometry(QtCore.QRect(160, 60, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_9.setFont(font)
        self.label_9.setLineWidth(1)
        self.label_9.setObjectName("label_9")
        self.Text_Id = QtWidgets.QLineEdit(add_Data)
        self.Text_Id.setGeometry(QtCore.QRect(360, 50, 261, 21))
        self.Text_Id.setObjectName("Text_Id")
        self.Text_name = QtWidgets.QLineEdit(add_Data)
        self.Text_name.setGeometry(QtCore.QRect(360, 100, 261, 21))
        self.Text_name.setObjectName("Text_name")
        self.Text_major = QtWidgets.QLineEdit(add_Data)
        self.Text_major.setGeometry(QtCore.QRect(360, 150, 261, 21))
        self.Text_major.setObjectName("Text_major")
        self.Text_star_year = QtWidgets.QLineEdit(add_Data)
        self.Text_star_year.setGeometry(QtCore.QRect(360, 200, 261, 21))
        self.Text_star_year.setObjectName("Text_star_year")
        self.Text_year = QtWidgets.QLineEdit(add_Data)
        self.Text_year.setGeometry(QtCore.QRect(360, 250, 261, 21))
        self.Text_year.setObjectName("Text_year")
        self.anh = QtWidgets.QFrame(add_Data)
        self.anh.setGeometry(QtCore.QRect(770, 50, 181, 171))
        font = QtGui.QFont()
        font.setItalic(False)
        self.anh.setFont(font)
        self.anh.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.anh.setFrameShadow(QtWidgets.QFrame.Raised)
        self.anh.setObjectName("anh")
        self.Add_anh = QtWidgets.QPushButton(add_Data)
        self.Add_anh.setGeometry(QtCore.QRect(800, 260, 93, 28))
        self.Add_anh.setObjectName("Add_anh")
        self.tableWidget = QtWidgets.QTableWidget(add_Data)
        self.tableWidget.setGeometry(QtCore.QRect(50, 330, 941, 192))
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName("tableWidget")
        self.Add_database = QtWidgets.QPushButton(add_Data)
        self.Add_database.setGeometry(QtCore.QRect(50, 560, 93, 28))
        self.Add_database.setObjectName("Add_database")
        self.Sua_database = QtWidgets.QPushButton(add_Data)
        self.Sua_database.setGeometry(QtCore.QRect(220, 560, 93, 28))
        self.Sua_database.setObjectName("Sua_database")
        self.Xoa_Database = QtWidgets.QPushButton(add_Data)
        self.Xoa_Database.setGeometry(QtCore.QRect(390, 560, 93, 28))
        self.Xoa_Database.setObjectName("Xoa_Database")
        self.Xuat_Database = QtWidgets.QPushButton(add_Data)
        self.Xuat_Database.setGeometry(QtCore.QRect(560, 560, 93, 28))
        self.Xuat_Database.setObjectName("Xuat_Database")
        self.Chup = QtWidgets.QPushButton(add_Data)
        self.Chup.setGeometry(QtCore.QRect(730, 560, 93, 28))
        self.Chup.setObjectName("Chup")
        self.Thoat = QtWidgets.QPushButton(add_Data)
        self.Thoat.setGeometry(QtCore.QRect(900, 560, 93, 28))
        self.Thoat.setObjectName("Thoat")

        self.tableWidget = QtWidgets.QTableWidget(add_Data)
        self.tableWidget.setGeometry(QtCore.QRect(50, 330, 941, 192))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Name", "Major", "Starting Year", "Year", "Total Attendance", "Last Attendance Time"])
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(2,90)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,70)
        self.tableWidget.setColumnWidth(5,130)
        self.tableWidget.setColumnWidth(6,200)
        self.load_data_to_table()

        self.retranslateUi(add_Data)
        QtCore.QMetaObject.connectSlotsByName(add_Data)

        self.Thoat.clicked.connect(add_Data.close)  # Kết nối nút Thoat với hàm đóng cửa sổ

        # Fix signal connection
        self.Add_database.clicked.connect(self.add_data_to_firebase)

        # Connect the button click event to the function
        self.Add_anh.clicked.connect(self.load_image)

        # Create QLabel to display the image
        self.image_label = QLabel(add_Data)
        self.image_label.setGeometry(QtCore.QRect(770, 50, 181, 171))
        self.image_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.image_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.image_label.setObjectName("image_label")

        # xuat encode
        self.Xuat_Database.clicked.connect(self.run_EncodeGenerator)

        # Connect the button click event to the function
        self.Xoa_Database.clicked.connect(self.delete_selected_data_from_firebase)

        # Connect the button click event to the function
        self.Sua_database.clicked.connect(self.show_selected_data)

        # Test chup hinh
        self.Chup.clicked.connect(self.run_Chuphinh)

    def run_Chuphinh(self):
        pathcur= "chup_hinh.py"
        os.system(f"python {pathcur}")

    def show_selected_data(self):
        # Lấy danh sách các dòng được chọn trong tableWidget
        selected_items = self.tableWidget.selectedItems()

        if len(selected_items) >= 7:
            # Lấy thông tin từ dòng được chọn
            student_id = selected_items[0].text()
            name = selected_items[1].text()
            major = selected_items[2].text()
            start_year = selected_items[3].text()
            year = selected_items[4].text()
            total_attendance = selected_items[5].text()
            last_attendance_time = selected_items[6].text()

            # Hiển thị thông tin lên các QLineEdit tương ứng
            self.Text_Id.setText(student_id)
            self.Text_name.setText(name)
            self.Text_major.setText(major)
            self.Text_star_year.setText(start_year)
            self.Text_year.setText(year)

            # Hiển thị ảnh từ Firebase Storage
            image_path = f"{student_id}.png"  # Loại bỏ "Images/" ở đây
            blob = bucket.blob(f"Images/{image_path}")  # Thêm "Images/" ở đây

            try:
                # Kiểm tra xem file đã tồn tại chưa
                if not os.path.exists(image_path):
                    # Tạo một file tạm thời để lưu ảnh từ Storage
                    with open(image_path, "wb") as file:
                        blob.download_to_file(file)

                # Hiển thị ảnh lên image_label
                pixmap = QtGui.QPixmap(image_path)
                self.image_label.setPixmap(pixmap.scaled(181, 171, QtCore.Qt.KeepAspectRatio))

                # Xoá file tạm thời
                os.remove(image_path)

                print("Selected data displayed successfully!")

            except Exception as e:
                print(f"Error downloading image from Storage: {str(e)}")

        else:
            print("Please select one row to display.")

    def delete_selected_data_from_firebase(self):
        # Lấy danh sách các dòng được chọn trong tableWidget
        selected_rows = set()
        for item in self.tableWidget.selectedItems():
            selected_rows.add(item.row())

        if selected_rows:
            for selected_row in sorted(selected_rows, reverse=True):
                # Lấy student_id từ dòng được chọn
                student_id = self.tableWidget.item(selected_row, 0).text()

                try:
                    # Xoá dữ liệu từ Firebase
                    ref = db.reference('Students')
                    ref.child(student_id).delete()

                    # Xoá ảnh từ Firebase Storage
                    image_path = f"Images/{student_id}.png"
                    blob = bucket.blob(image_path)
                    blob.delete()

                    print(f"Data for student with ID {student_id} deleted successfully!")
                    self.clear_input_fields()

                except Exception as e:
                    print(f"Error deleting data for student with ID {student_id}:", str(e))

            # Tải lại dữ liệu vào bảng
            self.load_data_to_table()

        else:
            print("Please select at least one row to delete.")


    def run_EncodeGenerator(self):
        # Lấy đường dẫn tương đối đến thư mục chứa add_data.py
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Tạo đường dẫn tương đối đến EncodeGenerator.py
        encode_generator_path = os.path.join(current_directory, "EncodeGenerator.py")

        # Chạy EncodeGenerator.py từ command line hoặc terminal
        os.system(f"python {encode_generator_path}")

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Cho phép người dùng chọn bất kỳ đường dẫn nào
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=options)

        if file_name:
            try:
                # Kiểm tra xem file có tồn tại không
                with open(file_name, "rb"):
                    pass

                # Hiển thị hình ảnh trên QLabel
                pixmap = QtGui.QPixmap(file_name)
                self.image_label.setPixmap(pixmap.scaled(181, 171, QtCore.Qt.KeepAspectRatio))

            except FileNotFoundError:
                print(f"File not found: {file_name}")

            except Exception as e:
                print(f"Error loading image: {str(e)}")

    def retranslateUi(self, add_Data):
        _translate = QtCore.QCoreApplication.translate
        add_Data.setWindowTitle(_translate("add_Data", "Form"))
        self.label.setText(_translate("add_Data", "name"))
        self.label_2.setText(_translate("add_Data", "major"))
        self.label_3.setText(_translate("add_Data", "starting_year"))
        self.label_4.setText(_translate("add_Data", "year"))
        self.label_7.setText(_translate("add_Data", "name"))
        self.label_9.setText(_translate("add_Data", "ID"))
        self.Add_anh.setText(_translate("add_Data", "Add"))
        self.Add_database.setText(_translate("add_Data", "Add"))
        self.Sua_database.setText(_translate("add_Data", "fix"))
        self.Xoa_Database.setText(_translate("add_Data", "Delete"))
        self.Xuat_Database.setText(_translate("add_Data", "encode"))
        self.Chup.setText(_translate("add_Data", "chụp"))
        self.Thoat.setText(_translate("add_Data", "exit"))

        _translate = QtCore.QCoreApplication.translate
        add_Data.setWindowTitle(_translate("add_Data", "Form"))
        self.label.setText(_translate("add_Data", "name"))

    def load_data_to_table(self):
        # Xóa toàn bộ dòng hiện tại trong tableWidget
        self.tableWidget.setRowCount(0)

        # Tải dữ liệu từ Firebase vào tableWidget
        ref = db.reference('Students')
        students_data = ref.get()

        if students_data:
            # Sắp xếp dữ liệu dựa trên student_id
            sorted_students = sorted(students_data.items(), key=lambda x: int(x[0]) if isinstance(x[0], str) and x[0].isdigit() else 0)

            for student_id, student_info in sorted_students:
                # Thêm dòng mới vào tableWidget
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

                # Thiết lập các Item cho từng ô trong dòng
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(student_id))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(student_info.get('name', '')))
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(student_info.get('major', '')))
                self.tableWidget.setItem(row_position, 3,
                                         QtWidgets.QTableWidgetItem(str(student_info.get('starting_year', ''))))
                self.tableWidget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(student_info.get('year', ''))))
                self.tableWidget.setItem(row_position, 5,
                                         QtWidgets.QTableWidgetItem(str(student_info.get('total_attendance', ''))))
                self.tableWidget.setItem(row_position, 6,
                                         QtWidgets.QTableWidgetItem(student_info.get('last_attendance_time', '')))

    def clear_input_fields(self):
        # Làm trắng lại các trường nhập liệu và image_label
        self.Text_Id.clear()
        self.Text_name.clear()
        self.Text_major.clear()
        self.Text_star_year.clear()
        self.Text_year.clear()
        self.image_label.clear()
    def add_data_to_firebase(self):
        # Lấy giá trị từ các trường nhập liệu
        student_id = self.Text_Id.text()
        name = self.Text_name.text()
        major = self.Text_major.text()

        # Handle the possibility of empty fields
        if not all([student_id, name, major]):
            print("Please fill in all fields.")
            return

        try:
            start_year = int(self.Text_star_year.text())
            year = int(self.Text_year.text())
        except ValueError:
            print("Starting Year and Year must be integers.")
            return

        # Tạo dữ liệu theo mẫu
        data = {
            "name": name,
            "major": major,
            "starting_year": start_year,
            "total_attendance": 0,
            "year": year,
            "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            # Thêm dữ liệu vào Firebase
            ref = db.reference('Students')
            ref.child(student_id).set(data)

            # Tải ảnh lên Firebase Storage
            image_path = f"{student_id}.png"
            pixmap = self.image_label.pixmap()
            if pixmap:
                pixmap.save(image_path)  # Save the pixmap as an image file

                with open(image_path, "rb") as file:
                    blob = bucket.blob(f"Images/{image_path}")
                    blob.upload_from_file(file, content_type="image/png")

                os.remove(image_path)  # Remove the temporary image file

                print("Data and image added successfully!")

                # Làm trắng lại các trường nhập liệu và image_label
                self.clear_input_fields()

                # Tải lại dữ liệu vào bảng
                self.load_data_to_table()

        except Exception as e:
            print("Error adding data to Firebase:", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    add_Data = QtWidgets.QWidget()
    ui = Ui_add_Data()
    ui.setupUi(add_Data)
    add_Data.show()
    sys.exit(app.exec_())
