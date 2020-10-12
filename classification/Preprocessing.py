import numpy as np 
import SimpleITK as sitk 
import csv
from classification.Prep_Instance import Prep_Instance


class Preprocessing:

    def __init__(self, csv_path): 
        """ csv contains path nifti and json with annotation
        """
        self.csv_path = csv_path
        self.dataset = self.extract_dataset()


    
    def extract_dataset(self):
        with open(self.csv_path, 'r') as csv_file :
            reader = csv.reader(csv_file, delimiter = ',') #liste pour chaque ligne 
            dataset = []
            for row in reader :
                dataset.append(row)
                
        del dataset[0] #enlever première ligne

        return dataset
        

    def normalize_encoding_dataset(self):
        liste = []
        label = []
        for serie in self.dataset : 
            instance_object = Prep_Instance(serie[1]) 
            instance_array = instance_object.ct_norm_array 
            liste.append(instance_array)
            
            #encoding
            subliste = instance_object.encoding_instance(serie)
            label.append(subliste)

        return np.asarray(liste), np.asarray(label)


