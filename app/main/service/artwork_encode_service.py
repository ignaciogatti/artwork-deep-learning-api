import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2  # for image processing


def get_image(nparr, img_Width=128, img_Height=128):
    #load image
    image = cv2.imdecode(nparr)
    image = cv2.resize(image, (img_Width, img_Height), interpolation=cv2.INTER_CUBIC)
    #normalize image
    image_norm = image * (1./255)
    image_norm = np.expand_dims(image_norm, axis=0)
    
    return image_norm

def predict(image_data):
    nparr = np.fromstring(image_data, np.uint8)
    image_norm = get_image(image_path)
    model = load_model('denoisy_encoder.h5')
    return model.predict(image_norm)
