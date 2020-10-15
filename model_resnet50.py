import SimpleITK as sitk 
import numpy as np 
import matplotlib.pyplot as plt 
from library_dicom.dicom_processor.tools.preprocessing import *
import json 
import csv 
from sklearn.model_selection import train_test_split 
import tensorflow as tf 
from classification.Prep_CSV import Prep_CSV
from classification.Preprocessing import Preprocessing 
from classification.resnet50 import *
import datetime
import os 

json_path = '/media/deeplearning/78ca2911-9e9f-4f78-b80a-848024b95f92/result.json'
nifti_directory = '/media/deeplearning/78ca2911-9e9f-4f78-b80a-848024b95f92'
objet = Prep_CSV(json_path)
objet.result_csv(nifti_directory)
print(objet.csv_result_path)

prep_objet = Preprocessing(objet.csv_result_path)
X, y = prep_objet.normalize_encoding_dataset()

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=1, test_size = 0.15)

print("size of X_train : ", X_train.shape)
print("size of y_train : ",y_train.shape)
print("")
print("size of X_test : ", X_test.shape)
print("size of y_test : ",y_test.shape)
#print("")
#print("size of X_val : ", X_val.shape)
#print("size of y_val : ",y_val.shape)


#model 
model = ResNet50(input_shape=(1024, 256, 1))
model.summary()
#compile 
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4) #param
model.compile(optimizer = optimizer, 
        loss={'left_arm' : 'sparse_categorical_crossentropy', 
            'right_arm' : 'sparse_categorical_crossentropy', 
             'head' : 'sparse_categorical_crossentropy', 
             'leg' : 'sparse_categorical_crossentropy'}, 
        loss_weights ={'left_arm': 0.25, 'right_arm' : 0.25, 
                        'head' : 0.25, 
                        'leg': 0.25}, 
        metrics = {'left_arm': ['accuracy'], #'SparseCategoricalCrossentropy'
                    'right_arm' : ['accuracy'], 
                    'head' : ['accuracy'], 
                    'leg':['accuracy']}) #a voir pour loss
log_dir = '/home/deeplearning/Dicom-To-CNN/Classification/Resnet/logs_15_10_2020'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, update_freq='epoch', write_graph=True, write_images=True)


"""
history = model.fit(X_train, {'head': y_train[:,0], 
                                    'leg': y_train[:,1],
                                    'right_arm' : y_train[:,2],
                                    'left_arm' : y_train[:,3] ,
                                    }, 
                                    
                        epochs = 50, 
                        batch_size = 32, 
                        verbose = 1, 
                        validation_split= 0.15,
                        #validation_data = (X_val, {'head': y_val[:,0], 
                                    #'leg': y_val[:,1],
                                    #'right_arm' : y_val[:,2],
                                    #'left_arm' : y_val[:,3] ,
                                    #}))
                        callbacks=[tensorboard_callback])

#print(y_val)
#predictions = model.predict(X_val[0:10])
#print("Predictions done !")
#print(predictions)
#from classification.resnet50 import predictions_decoding 
#predi = predictions_decoding(predictions)
#print(predi)

"""
#save 
folder = '/media/deeplearning/78ca2911-9e9f-4f78-b80a-848024b95f92/Classification/Resnet'
if not os.path.exists(folder) : 
    os.makedirs(folder)
#model.save(folder + '/' + 'resnet_model', save_format='h5')