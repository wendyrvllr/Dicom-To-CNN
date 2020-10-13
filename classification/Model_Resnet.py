import numpy as np 
from sklearn.model_selection import train_test_split 
from classification.Preprocessing import Preprocessing
import tensorflow as tf
from tensorflow.keras.applications import ResNet50 
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Flatten
from tensorflow.keras.models import Model 
import matplotlib.pyplot as plt 





class Model_Resnet: 

    def __init__(self, data, label):
        self.data = data   
        self.label = label 
        self.X_train, self.y_train, self.X_test, self.y_test, self.X_val, self.y_val = self.split_dataset()


    def split_dataset(self) : 
        X_train, X_test, y_train, y_test = train_test_split(self.data, self.label, random_state = 0, test_size=0.2)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state = 0, test_size=0.2)

        return X_train, y_train, X_test, y_test, X_val, y_val
    
    #architecture 

    def resnet_model(self, X_train):
        base_model = ResNet50(include_top = False, weights ="None", input_shape = (1024, 256, 1), pooling='max')
        #revoir architecture fin réseau
        base_model.summary()
        #for layer in base_model.layers : 
            #print(layer)
            #layer.trainable = True 

        #layer[]
        #voir pour faire sur toutes les layers, pq ? 


        x = base_model.output
        print(x.shape)
        x = Flatten()(x)
        print(x.shape)

        #output 
        left_arm = Dense(2, activation='softmax', name='left_arm')(x)
        right_arm = Dense(2, activation='softmax', name = 'right_arm')(x)

        head = Dense(3, activation='softmax', name='head')(x)
        leg = Dense(3, activation='softmax', name='leg')(x)

        model = Model(inputs = X_train, outputs = [left_arm, right_arm, head, leg], name='ResNet50' )
        return model 

    
    def model_summary(self, model):
        model.summary 

    def model_compile(self, model):
        optimizer = tf.keras.optimizers.SGD(learning_rate=1e-5) #param
        #loss = tf.keras.losses.CategoricalCrossentropy(#param)
        model.compile(optimizer =optimizer, loss={'left_arm' : 'binary_crossentropy', 
                                                    'right_arm' : 'binary_crossentropy', 
                                                    'head' : 'binary_crossentropy', 
                                                    'leg' : 'binary_crossentropy'}, 
                                                        
                                                    loss_weights ={'left_arm': 0.25, 
                                                                    'right_arm' : 0.25, 
                                                                    'head' : 0.25, 
                                                                    'leg': 0.25}, 
                                                                    
                                                    metrics = {'left_arm': ['accuracy', 'BinaryCrossentropy'], 
                                                                'right_arm' : ['accuracy', 'BinaryCrossentropy'], 
                                                                'head' : ['accuracy','BinaryCrossentropy'], 
                                                                'leg':['accuracy','BinaryCrossentropy']}) #a voir pour loss
    
    def model_fit(self, model):
        history = model.fit(self.X_train, {'head': self.y_train[:,2], 
                                    'leg': self.y_train[:,3],
                                    'right_arm' : self.y_train[:,1],
                                    'left_arm' : self.y_train[:,0] ,
                                    }, 
                                    
                        epochs = 10, 
                        batch_size = 200, 
                        verbose = 1, 
                        validation_data = (self.X_val, self.y_val))

        return history 

    def model_predict(self, model, X):
        prediction = model.predict(X)

        return prediction 

    def show_training_curves(self, model) : 
        history = self.model_fit(model)
        #accuracy
        f = plt.figure(figsize=(8,5))
        axes = plt.gca()
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'])
        plt.show() 

        #loss
        f = plt.figure(figsize=(8,5))
        axes = plt.gca()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'])
        plt.show() 
        return None 












    