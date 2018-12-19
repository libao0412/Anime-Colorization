##### This is a collection of functions I used for processing images.

##### Importing function

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from skimage.color import rgb2lab, lab2rgb, rgb2gray, xyz2lab


##### function transforming from RGB to LAB image

def rgb_lab_transformation(image_resized, image_size):
    
    # create 3 dimensional gray image with rgb2gray * 3
    image_gray = rgb2gray(image_resized).reshape(image_size[0], image_size[1], 1) # this will be the validation dataset
    image_gray3 = np.concatenate([image_gray]*3, axis = 2)
    image_lab3 = rgb2lab(image_gray3)
    image_feature = image_lab3[:,:,0]/128 # scaling from -1 to 1 based on LAB space value range

    # create label first with rgb2lab image
    image_lab = rgb2lab(image_resized)
    image_label = image_lab[:,:,1:]/128 # scaling from -1 to 1 based on LAB space value range
    
    return image_feature, image_label # return feature would be 1st column of lab image generated by gray3 image

##### Function creating individual feature and label
def feature_label_generation(character_dir, filename_list, image_size):
    
    feature = []
    label = []
    
    for filename_num in range(len(filename_list)):
    
        image_chosen = cv2.resize(plt.imread(character_dir + filename_list[filename_num]), image_size)

        if image_chosen.shape[2] == 3:

            feature_indiv, label_indiv = rgb_lab_transformation(image_chosen, image_size)

            feature.append(feature_indiv)
            label.append(label_indiv)

    return feature, label

###### Function creating train and test dataset

def data_generation(dir_name, image_size, test_size = 0.3, single_character = None):

    # creating dictionaries

    folder_name = os.listdir(dir_name)

    character_name = [i[4:] for i in folder_name]
    character_name.sort()

    folder_dict = {}

    for i in range(len(folder_name)):
        folder_dict[folder_name[i][4:]] = folder_name[i]

    image_dict = {}

    for i in range(len(folder_name)):

        file_list = os.listdir(dir_name + folder_name[i])
        image_list = [i for i in file_list if i[-3:] == 'png']

        image_dict[folder_name[i][4:]] = image_list

    label_dict = {}

    for i in range(len(folder_name)):
        label_dict[folder_name[i][4:]] = i

    label_dict_inv = {v: k for k, v in label_dict.items()}

    # creating lists and appending

    if single_character != None: # whether to use images of only one character or all characters
        character_name = [single_character]

    train_image_all = []
    test_image_all = []
    train_label_all = []
    test_label_all = []
        
    for i in range(len(character_name)):

        print(str(i+1) +'/'+str(len(character_name)))

        image_file = image_dict[character_name[i]]

        train_index, test_index = train_test_split(np.arange(len(image_file)), test_size = test_size)

        train_list = np.array(image_file)[list(train_index)]
        test_list = np.array(image_file)[list(test_index)]
        
        character_dir = dir_name + '{}/'.format(folder_dict[character_name[i]])

        train_image, train_label = feature_label_generation(character_dir, train_list, image_size = image_size)
        train_image_all += train_image
        train_label_all += train_label
        
        test_image, test_label = feature_label_generation(character_dir, train_list, image_size = image_size)
        test_image_all += test_image
        test_label_all += test_label
        
    return np.array(train_image_all), np.array(test_image_all), np.array(train_label_all), np.array(test_label_all)