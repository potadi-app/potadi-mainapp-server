import tensorflow as tf
from .utils.model_loader import ModelLoader
from .utils.image_processing import preprocess_image

def predict_disease_h5(image):
    """Predicts the disease of a potato leaf using a .h5 model.
    Args:
        image: The uploaded potato leaf image.
    Returns:
        dict:
            A dictionary containing the disease label and confidence.
    """
    
    try:
        processed_image = preprocess_image(image)
        
        model = ModelLoader.load_trained_model()
        
        prediction = model.predict(processed_image)[0]
        
        probabilities  = {
            'early_blight': prediction[0],
            'healthy': prediction[1],
            'late_blight': prediction[2]
        }
        
        probabilities = {k: round(v * 100, 2) for k, v in probabilities.items()}
        
        label, confidence = convert_prediction_to_label(probabilities)
        
        return {
            'label': label,
            'confidence': confidence,
            'probabilities': probabilities
        }
    except Exception as e:
        raise Exception(f'Error while predicting: {e}')

def predict_disease_saved_model(image, version=1):
    """Predicts the disease of a potato leaf using a saved model.
    Args:
        image: The uploaded potato leaf image.
    Returns:
        dict:
            A dictionary containing the disease label and confidence.
    """
    
    try:
        processed_image = preprocess_image(image)
        
        model = ModelLoader.load_saved_model(version=version)
        infer = model.signatures["serving_default"]
        
        # Ensure the image tensor has the correct shape
        input_tensor = tf.convert_to_tensor(processed_image, dtype=tf.float32)
        
        # Perform the inference
        prediction = infer(input_tensor)

        # Adjust this line based on the actual output of the model
        prediction_output = prediction['dense_1'] if 'dense_1' in prediction else list(prediction.values())[0]
        
        # Assuming prediction_output is a tensor of shape [1, num_classes]
        probabilities = {
            'early_blight': prediction_output[0][0].numpy(),
            'healthy': prediction_output[0][1].numpy(),
            'late_blight': prediction_output[0][2].numpy()
        }
        
        probabilities = {k: round(v * 100, 2) for k, v in probabilities.items()}
        
        label, confidence = convert_prediction_to_label(probabilities)
        
        return {
            'label': label,
            'confidence': confidence,
            'probabilities': probabilities
        }
    except Exception as e:
        raise Exception(f'Error while predicting: {e}')


def convert_prediction_to_label(probabilities: dict) -> tuple:
    """
    Converts the prediction result into an understandable label based on the highest probability.
    :param probabilities: Probabilities for each label.
    :return: Disease label and highest confidence score.
    """
    label = max(probabilities, key=probabilities.get)  # Get the label with the highest confidence
    confidence = probabilities[label]  # Highest confidence value
    return label, confidence