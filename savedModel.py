import tensorflow as tf

model = tf.keras.models.load_model('diagnose/model/model_MobileNet_imagenet_New_224.h5')
model.load_weights('diagnose/model/weights_MobileNet_imagenet_New_224.h5')
tf.saved_model.save(model, 'diagnose/model/savedModel/v2')
