# Der Code in dieser Datei kommt von der Master Arbeit von Herr Valeri Asmus
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
model_dir = 'Classification/lecture_fcl.h5'
model = load_model(model_dir)
dict1 = {0: 'Fault', 1: 'Others', 2: 'Professor', 3: 'Slides', 4: 'Whiteboard'}

# Construct path dictionary of dir + all images in
def get_image_paths(lecture_dir):
    dirs = [x[0] for x in os.walk(lecture_dir)]
    path_dict = {}
    index = 0
    for dir in dirs:
        if index != 0:  # first is base dir, not needed
            images = []
            for file in os.listdir(dir):
                ext = os.path.splitext(file)[1]
                # only .jpg
                if ext.lower() == ".jpg":
                    images.append(file)
            path_dict[dir] = images
        index = index + 1
    return path_dict

def get_prediction_on_scene(key, value, model):
    prediction_dict = {}
    image_full_paths = []
    scene_dir = key
    imagenames = value
    # concatenate scene_dir and image path
    for imagename in imagenames:
        image_full_paths.append(os.path.join(scene_dir, imagename))

    # get predict for each scene
    seq_index = 1
    scene_index = 1
    temp_pred = []
    for img_path in image_full_paths:
        img = image.load_img(img_path, target_size=(224, 224))
        img_tensor = image.img_to_array(img)  # Image data encoded as integers in the 0–255 range
        img_tensor /= 255.  # Normalize to [0,1]
        test_image = np.expand_dims(img_tensor, axis=0)
        # Extract features
        result = model.predict(test_image)
        res = np.argmax(result)
        temp_pred.append(dict1[res])
        prediction_dict[scene_index] = dict1[res]
        if seq_index % 3 == 0:
            # compute test of three image of each scene
            if (temp_pred[0] == temp_pred[1] == temp_pred[2]) | (temp_pred[0] == temp_pred[1]) | (
                    temp_pred[0] == temp_pred[2]):
                prediction_dict[scene_index] = temp_pred[0]
            elif (temp_pred[1] == temp_pred[2]):
                prediction_dict[scene_index] = temp_pred[1]
            else:
                prediction_dict[scene_index] = 'N/A'
            scene_index = scene_index + 1
            temp_pred = []
        seq_index = seq_index + 1
    return prediction_dict

def executeSceneClassification(path):
    image_paths_dict = get_image_paths(path)
    print("execute scene classification in %s"%path)
    print(image_paths_dict)
    prediction=[]
    for key, value in image_paths_dict.items():
        prediction = get_prediction_on_scene(key, value, model)
    return prediction
