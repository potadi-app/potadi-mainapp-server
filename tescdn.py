from cloudinary import uploader

try:
    result = uploader.upload("diagnoses/user@example.com/Late_5.jpg")
    print(result)
except Exception as e:
    print(f"Error uploading to Cloudinary: {e}")
