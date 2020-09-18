import numpy as np 
from sklearn.model_selection import train_test_split 
from classification.Preprocessing import Preprocessing
import tensorflow as tf
from tensorflow.keras.applications import ResNet50 
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Flatten
from tensorflow.keras.models import Model 

class Model_Resnet: 

    def __init__(self, csv_path):
        pass 
        objet = Preprocessing(csv_path)
        self.X, self.y = objet.normalize_encoding_dataset()

        self.X_train, self.y_train, self.X_test, self.y_test, self.X_val, self.y_val = self.split_dataset()


    def split_dataset(self) : 
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, random_state = 0, test_size=0.2)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state = 0, test_size=0.2)

        return X_train, y_train, X_test, y_test, X_val, y_val
    
    #architecture 

    def resnet_model(self):
        base_model = ResNet50(weigths = 'imagenet', include_top = False, input_tensor = [1024,256], pooling='max')
        #revoir architecture fin réseau
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Flatten()(x)

        left_arm = Dense(2, activation='softmax', name='left_arm')(x)
        right_arm = Dense(2, activation='softmax', name = 'right_arm')(x)

        head = Dense(3, activation='softmax', name='head')(x)
        leg = Dense(3, activation='softmax', name='leg')(x)

        model = Model(inputs = self.X, outputs = [left_arm, right_arm, head, leg], name='ResNet50' )

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
                                                                    
                                                    metrics = {'left_arm': ['accuracy'], 
                                                                'right_arm' : ['accuracy'], 
                                                                'head' : ['accuracy'], 
                                                                'leg':['accuracy']}) #a voir pour loss
    
    def model_fit(self, model):
        history = model.fit(self.X_train, {'left_arm' : self.y_train[:,0],
                                    'right_arm' : self.y_train[:,1] ,
                                    'head': self.y_train[:,2], 
                                    'leg': self.y_train[:,3]}, 
                                    
                        epochs = 10, 
                        batch_size = 200, 
                        verbose = 2, 
                        validation_data = (X_val, y_val))

        return history 

    def model_predict(self, model, X):
        prediction = model.predict(X)

        return prediction 

    def show_training_curves(self, model) : 
        history = self.model_fit(model)
        display_training_curves(history.history['accuracy'], history.history['val_accuracy'], 'accuracy', 211)
        display_training_curves(history.history['loss'], history.history['val_loss'], 'loss', 212)
        return None 












    