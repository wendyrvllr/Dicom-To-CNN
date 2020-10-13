import numpy as np 
import SimpleITK as sitk 
import json 

class Prep_Instance : 

    def __init__(self, ct_img_path):
        self.ct_img = sitk.ReadImage(ct_img_path)
        self.ct_array = sitk.GetArrayFromImage(self.ct_img)

        self.ct_norm_img = self.normalize_instance()
        self.ct_norm_array = sitk.GetArrayFromImage(self.ct_norm_img)
        self.ct_norm_array = np.reshape(self.ct_norm_array, (1024, 256, 1))


    def normalize_instance(self):
        intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
        intensityWindowingFilter.SetOutputMaximum(1)
        intensityWindowingFilter.SetOutputMinimum(0)
        new_img = intensityWindowingFilter.Execute(self.ct_img)

        return new_img 

    #ici mettre methode encodage pour une instance 
    def encoding_instance(self, liste):
        label = []
    
        #upper Limit 
        if liste[2] == 'Vertex' : 
            label.append(0)
        if liste[2] == 'Eye' : 
            label.append(1)
        if liste[2] == 'Mouth':
            label.append(2)

        #lower Limit
        if liste[3] == 'Hips' : 
            label.append(0)
        if liste[3] == 'Knee' : 
            label.append(1)
        if liste[3] == 'Foot':
            label.append(2)

        #right Arm 
        if liste[4] == 'down' : 
            label.append(0)
        if liste[4] == 'up' : 
            label.append(1)

        #left Arm 
        if liste[5] == 'down' : 
            label.append(0)
        if liste[5] == 'up' : 
            label.append(1)

        return label