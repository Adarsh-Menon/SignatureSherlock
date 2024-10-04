import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2


def load_model():
    model = tf.keras.models.load_model('image.hdf5')
    return model

def predict_class(image, model):
        image = Image.open(image)
        resized_image = image.resize((224, 224))
        grayscale_image = resized_image.convert('L')
        img_array = np.array(grayscale_image)
        img = img_array.reshape(-1, 224, 224, 1) / 255.0
        prediction = model.predict(img)
        return prediction[0][0]

model = load_model()
st.title('Signature Sherlock : Handwritten Signature Classifier')

file = st.file_uploader("Upload an image of a signature", type=["jpg", "png"])

if file is None:
    st.text('Waiting for upload....')
else:
    slot = st.empty()
    slot.text('Running inference....')

    test_image = Image.open(file)
    st.image(test_image, caption="Input Image", width=400)

    pred = predict_class(file, model)
    st.text(f'Prediction Probability: {pred}')

    if pred < 0.4998:
        result = "real"
    else:
        result = "forged"

    output = 'The signature is ' + result
    slot.text('Done')
    st.success(output)
