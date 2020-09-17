import numpy as np 
from sklearn.model_selection import train_test_split 
from classification.Preprocessing import Preprocessing
import tensorflow as tf

class Model : 

    def __init__(self, csv_path):
        pass 
        objet = Preprocessing(csv_path)
        self.X, self.y = objet.normalize_encoding_dataset()

    def split_dataset(self) : 
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, random_state = 0, test_size=0.2)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state = 0, test_size=0.2)

        return X_train, y_train, X_test, y_test, X_val, y_val
    
    #architecture 
    