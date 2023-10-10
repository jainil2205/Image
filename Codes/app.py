import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_size', methods=['POST'])
def calculate_size():
    print("Python code reached")
    if 'image' not in request.files:
        return "No image file provided", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No selected image file", 400

    try:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        # Calculate the size of the image
        image_size = os.path.getsize(image_path)
        print("Image size:", image_size, "bytes")

    
        label_map = { 'Ajanta Caves': 0,
            'Charar-E- Sharif': 1,
            'Chhota_Imambara': 2,
            'Ellora Caves': 3,
            'Fatehpur Sikri': 4,
            'Gateway of India': 5,
            'Hawa mahal': 6,
            'Humayun_s Tomb': 7,
            'India_gate': 8,
            'Khajuraho': 9,
            'Sun Temple Konark': 10,
            'alai_darwaza': 11,
            'alai_minar': 12,
            'basilica_of_bom_jesus': 13,
            'charminar': 14,
            'golden temple': 15,
            'iron_pillar': 16,
            'jamali_kamali_tomb': 17,
            'lotus_temple': 18,
            'mysore_palace': 19,
            'qutub_minar': 20,
            'tajmahal': 21,
            'tanjavur temple': 22,
            'victoria memorial': 23
        }

        loaded_model = tf.keras.models.load_model('D:\Downloads\Codes\my_model.h5')

        # Creating a sample inference function
        def prediction(image_path, model):
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
            x = tf.keras.preprocessing.image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            #print('Predictions', preds)
            
            for pred, value in label_map.items():    
                if value == np.argmax(preds):
                    print('Predicted class is:', pred)
                    print('With a confidence score of: ', np.max(preds))
            
            return np.argmax(preds)

        monument_list = ['Ajanta Caves', 'Charar-E-Sharif', 'Chhota_Imambara', 'Ellora Caves','Fatehpur Sikri', 'Gateway of India', 'Hawa mahal', 'Humayun_s Tomb','India_gate', 'Khajuraho', 'Sun Temple Konark', 'alai_darwaza','alai_minar', 'basilica_of_bom_jesus', 'charminar', 'golden temple','iron_pillar', 'jamali_kamali_tomb', 'lotus_temple', 'mysore_palace','qutub_minar', 'tajmahal', 'tanjavur temple', 'victoria memorial']


        x=image_file
        monument = str(prediction(image_path, loaded_model))
        # print(monument_list[int(monument)-1])
        return f"Predicted Monument: {monument_list[int(monument)]}"

        # return str(image_size)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)