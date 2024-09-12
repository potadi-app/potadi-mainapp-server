from keras.models import load_model
from core.settings import BASE_DIR

def load_trained_model():
    """
    Load the trained model.
    :return: The trained model.
    """
    model = load_model(f"{BASE_DIR}/diagnose/model/model_MobileNet_imagenet_New_224.h5")
    model.load_weights(f"{BASE_DIR}/diagnose/model/weights_MobileNet_imagenet_New_224.h5")
    return model