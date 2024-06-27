import json
from flask import request, jsonify
from helpers.class_names import class_names
from helpers.generate_pdf import generate_classification_report
from helpers.is_plant import is_plant
from helpers.upload_images import upload_file
from werkzeug.utils import secure_filename

import tensorflow as tf
import numpy as np

from models.model import add_model_data


def classify_image(email):
    if 'file' not in request.files:
        return jsonify({"status": False, 'message': 'No file part in the request', 'data': None}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": False, 'message': 'No file selected for uploading', 'data': None}), 400

    plantPath = upload_file('file', 'plants')
    filename = secure_filename(file.filename)

    if (not is_plant('public/plants/' + filename)):
        return jsonify(
            {
                "status": False,
                "message": "Image is not a plant",
                "data": {
                    'predictions': "Image is not a plant",
                    "image": plantPath,
                }
            }), 200

    model = tf.keras.models.load_model(
        './models/my_model.h5')
    img_path = 'public/plants/' + filename
    img = tf.keras.preprocessing.image.load_img(
        img_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    confidence = round(100*(np.max(prediction[0])), 2)

    finall_class = class_names()[np.argmax(prediction)]
    with open("./helpers/data.json", 'r') as file:
        plants_data = json.load(file)

    discription = plants_data[finall_class.split(' ')[0]]["discription"]
    temperature = plants_data[finall_class.split(' ')[0]]["temperature"]
    sunlight = plants_data[finall_class.split(' ')[0]]["sunlight"]
    watering = plants_data[finall_class.split(' ')[0]]["watering"]
    add_model_data(predictions=finall_class, confidence=confidence, image=plantPath, discription=discription,
                   temperature=temperature, sunlight=sunlight, watering=watering, userEmail=email)
    report = generate_classification_report(
        [finall_class, confidence, discription, temperature, sunlight, watering, email])
    return jsonify(
        {
            "status": True,
            "message": "Image classified successfully",
            "data": {
                'predictions': finall_class,
                "confidence": confidence,
                "image": plantPath,
                "discription": discription,
                "temperature": temperature,
                "sunlight": sunlight,
                "watering": watering,
                "report_path": report
            }
        }), 200
