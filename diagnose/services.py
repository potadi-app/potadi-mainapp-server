import requests
import os

def predict_disease_saved_model(image, version=1):
    """Predicts the disease of a potato leaf using a saved model.
    Args:
        version: Version of the model (default is 1).
    Returns:
        dict:
            A dictionary containing the disease label and confidence.
    """
    
    url = f'{os.getenv("FASTAPI_SERVER_URL")}/api/diagnose'
    try:
        # Make the POST request to the FastAPI server
        response = requests.post(url, files={'image': image})
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return response.text

    except Exception as e:
        raise Exception(f'Error while predicting: {e}')
