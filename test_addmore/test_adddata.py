import firebase_admin
from firebase_admin import credentials, db, storage
from PIL import Image
import os
# Initialize Firebase
cred = credentials.Certificate("testfacedlib.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://test-11ecb-default-rtdb.firebaseio.com/",
    'storageBucket': "test-11ecb.appspot.com"
})

# Function to upload images from a directory to Firebase Storage and update the database
def upload_images_and_student_data(directory_path, user_id, student_data):
    # Reference to the storage bucket
    bucket = storage.bucket()

    # Create a dictionary to store image URLs
    image_urls = {}

    # Create a folder with the user_id as the name in Firebase Storage
    user_folder = f"{user_id}/"
    user_blob = bucket.blob(user_folder)

    # Make the folder (if it doesn't exist)
    user_blob.upload_from_string("")

    # Iterate through files in the directory
    for i, filename in enumerate(os.listdir(directory_path), 1):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(directory_path, filename)

            # Open and resize the image to 220x220
            img = Image.open(image_path)
            img = img.resize((220, 220))

            # Save the resized image in PNG format
            resized_image_path = os.path.join(directory_path, f"{user_id}_{i}.png")
            img.save(resized_image_path, "PNG")

            # Upload the resized image to the user's folder in the storage bucket
            image_name = f"{user_folder}{user_id}_{i}.png"
            blob = bucket.blob(image_name)
            blob.upload_from_filename(resized_image_path)

            # Get the URL of the uploaded image
            image_url = blob.public_url
            image_urls[f'ảnh{i}'] = image_url

    # Update the database with the student data excluding image_urls
    student_data_with_images = {
        user_id: {
            "name": student_data[user_id]["name"],
            "major": student_data[user_id]["major"],
            "starting_year": student_data[user_id]["starting_year"],
            "total_attendance": student_data[user_id]["total_attendance"],
            "year": student_data[user_id]["year"],
            "last_attendance_time": student_data[user_id]["last_attendance_time"]
        }
    }
    db.reference('Students').update(student_data_with_images)

# Student data
student_data = {
    "162001571": {
        "name": "Pham huu tien tai",
        "major": "IT",
        "starting_year": 2018,
        "total_attendance": 5,
        "year": 3,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
}

# Base directory containing subdirectories
base_directory = r'D:\1test\Du_An_ung_dung\test_addmore\face'

# Automatically discover subdirectories and process them
for subdirectory_name in os.listdir(base_directory):
    subdirectory_path = os.path.join(base_directory, subdirectory_name)
    if os.path.isdir(subdirectory_path):
        user_id = subdirectory_name
        upload_images_and_student_data(subdirectory_path, user_id, student_data)
