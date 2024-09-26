import tensorflow as tf
from keras.models import load_model
from core.settings import BASE_DIR


class ModelLoader:
    _model_h5 = None
    _model_saved = None

    @staticmethod
    def load_trained_model():
        """
        Load the trained model.
        :return: The trained model.
        """
        if ModelLoader._model_h5 is None:
            ModelLoader._model_h5 = load_model(f"{BASE_DIR}/diagnose/model/model_MobileNet_imagenet_New_224.h5")
            ModelLoader._model_h5.load_weights(f"{BASE_DIR}/diagnose/model/weights_MobileNet_imagenet_New_224.h5")
        
        return ModelLoader._model_h5
    
    @staticmethod
    def load_saved_model(version=1):
        """
        Load the trained model from SavedModel format.
        :return: The trained model.
        """
        if ModelLoader._model_saved is None:
            ModelLoader._model_saved = tf.saved_model.load(f"{BASE_DIR}/diagnose/model/savedModel/v{version}")
        
        return ModelLoader._model_saved