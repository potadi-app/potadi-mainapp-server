import numpy as np
from PIL import Image

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess the image to match the model input. Resize and normalize the image.
    :image param: The original image.
    :param target_size: The target size corresponding to the model input.
    :return: The image in the form of a numpy array ready to be used for prediction.
    """
    
    img = Image.open(image).convert('RGB') # Open the image and convert it to RGB
    img = img.resize(target_size) # Resize the image
    img_array = np.array(img) # Normalize the image
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
    
    return img_array
    