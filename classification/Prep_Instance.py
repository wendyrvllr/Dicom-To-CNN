import numpy as np 
import SimpleITK as sitk 
import json 

class Prep_Instance : 

    def __init__(self, ct_img_path, json_path):
        self.ct_img = sitk.ReadImage(ct_img_path)
        self.ct_array = sitk.GetArrayFromImage(self.ct_img)

        self.ct_norm_img = self.normalize_instance()
        self.ct_norm_array = sitk.GetArrayFromImage(self.ct_norm_img)

        self.json_path = json_path

    def normalize_instance(self):
        intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
        intensityWindowingFilter.SetOutputMaximum(1)
        intensityWindowingFilter.SetOutputMinimum(0)
        new_img = intensityWindowingFilter.Execute(self.ct_img)

        return new_img 

    #ici mettre methode encodage pour une instance 
    def encoding_instance(self):
        annot = []
        with open(self.json_path) as json_file : 
            reader = json.load(json_file)
            for info in reader :
                annot.append(info)

        label = np.zeros((1,10))

        #if label dans annot json, on met un 1 


        return label