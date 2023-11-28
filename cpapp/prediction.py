from __future__ import division, print_function
from unittest import result

import numpy as np


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array


labels= {'covid':0,"normal":1,"pneumonia":2}
## loading the saved model
model= load_model("model.h5")

def model_predict(new_scr):
    img = load_img(str(new_scr), target_size=(256, 256))
    # plt.imshow(img)
    img = img_to_array(img)
    # img = img / 255
    # print(img, img.shape)

    img = img.reshape(1, 256, 256, 3)
    result = model.predict(img)
    print(result)
    preds1 = np.argmax(result, axis=1)
    print(preds1)
    if preds1==0:
        preds1 = "You are diagnosed with covid please consult a doctor"
    elif preds1==1:
        preds1 = "You are a healthy person"
    elif preds1==2:
        preds1 = "You have pneumonia"

    return preds1
