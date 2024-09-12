from .utils.model_loader import load_trained_model
from .utils.image_processing import preprocess_image

def predict_disease(image):
    """
    Take an image of a potato leaf, perform disease prediction using the trained model.
    :param image: The uploaded potato leaf image.
    :return: Disease label and confidence.
    """
    
    try:
        processed_image = preprocess_image(image)
        
        model = load_trained_model()
        
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
    
def convert_prediction_to_label(probabilities: dict) -> tuple:
    """
    Converts the prediction result into an understandable label based on the highest probability.
    :param probabilities: Probabilities for each label.
    :return: Disease label and highest confidence score.
    """
    label = max(probabilities, key=probabilities.get)  # Get the label with the highest confidence
    confidence = probabilities[label]  # Highest confidence value
    return label, confidence