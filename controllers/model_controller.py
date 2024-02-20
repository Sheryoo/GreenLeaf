from flask import request, jsonify
from helpers.class_names import class_names
from helpers.upload_images import upload_file
from werkzeug.utils import secure_filename

import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np


def classify_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    plantPath = upload_file('file', 'plants')
    filename = secure_filename(file.filename)

    model = tf.keras.models.load_model(
        './models/my_model.h5')
    img_path = 'public/plants/' + filename
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    confidence = round(100*(np.max(prediction[0])), 2)
    finall_class = class_names()[np.argmax(prediction)]
    
    return jsonify({"status": True, "message": "success", "data": {'predictions': finall_class, "confidence": confidence, "image": plantPath}}), 200
