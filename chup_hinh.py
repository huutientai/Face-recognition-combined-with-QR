import cv2
import os
import random

# Tên thư mục để lưu hình ảnh
output_folder = "captured_images"

# Tạo thư mục nếu nó chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Mở kết nối với camera (0 là camera mặc định)
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera có được mở không
if not cap.isOpened():
    print("Không thể mở camera.")
    exit()

while True:
    # Đọc dữ liệu từ camera
    ret, frame = cap.read()
    # Hiển thị hình ảnh từ camera
    cv2.imshow("Camera", frame)
    filename = "captured_images/image_{}.jpg".format(random.randint(1, 10000))
    # Kiểm tra xem phím c hoặc q có được nhấn không
    key = cv2.waitKey(1)
    if key == ord('c'):
        # Lưu hình ảnh vào thư mục
        cv2.imwrite(filename, frame)
        print(f"Hình ảnh đã được lưu vào: {filename}")

    elif key == ord('q'):
        # Nếu phím q được nhấn, thoát khỏi vòng lặp
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
