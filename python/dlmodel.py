import numpy as np
import matplotlib.pyplot as plt

import cv2 # imported from Open
from tensorflow.keras.models import load_model

class Model():

    # BW REMOVE BELOW AS DEFAULT
    # def __init__(self, drImage):
    #     self.drImage = drImage

    def runInference(self,dlImage):
        # load model
        model = load_model("python/malaria-cell-cnn.h5")
        # # summarize model.
        # #model.summary()

        # # testing images
        # BW for testing
        # "static\uploads\C1_thinF_IMG_20150604_104919_cell_123.png"
        cell2infer = "static/uploads/" + dlImage
        # cell2infer =   "testing-samples/C1_thinF_IMG_20150604_104919_cell_123.png"  # dlImage #
        # BW USE BELOW AS DEFAULT
        # cell2infer =  "testing-samples/C1_thinF_IMG_20150604_104919_cell_123.png" 
        # # infected_cell = "testing-samples/C33P1thinF_IMG_20150619_121503a_cell_159.png"

        # # _, ax = plt.subplots(1, 2)
        # # ax[0].imshow(plt.imread(uninfected_cell))
        # # ax[0].title.set_text("Uninfected Cell")
        # # ax[1].imshow(plt.imread(infected_cell))
        # # ax[1].title.set_text("Parasitized Cell")
        # #plt.show()

        img_size=70

        # # load above images and perform preprocessing:
        cell2infer_arr = cv2.imread(cell2infer, cv2.IMREAD_GRAYSCALE)
        # # img_arr_infected = cv2.imread(infected_cell, cv2.IMREAD_GRAYSCALE)
        # # resize the images to (70x70)
        cell2infer_arr = cv2.resize(cell2infer_arr, (img_size, img_size))
        # # img_arr_infected = cv2.resize(img_arr_infected, (img_size, img_size))
        # # scale to [0, 1]
        # # img_arr_infected = img_arr_infected / 255
        cell2infer_arr = cell2infer_arr / 255
        # # reshape to fit the neural network dimensions
        # # (changing shape from (70, 70) to (1, 70, 70, 1))
        # # img_arr_infected = img_arr_infected.reshape(1, *img_arr_infected.shape)
        # # img_arr_infected = np.expand_dims(img_arr_infected, axis=3)
        cell2infer_arr = cell2infer_arr.reshape(1, *cell2infer_arr.shape)
        cell2infer_arr = np.expand_dims(cell2infer_arr, axis=3)

        # # perform inference
        # # infected_result = model.predict(img_arr_infected)[0][0]
        cell2infer_arr = model.predict(cell2infer_arr)[0][0]
        # #print(f"Infected: {infected_result}")
        # #print(f"Uninfected: {uninfected_result}")
        return cell2infer_arr

