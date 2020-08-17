import numpy as np
import SimpleITK as sitk 
import matplotlib.pyplot as plt
import scipy as sc
from sklearn import mixture
from library_dicom.post_processing.Mask3D import Mask3D
from library_dicom.post_processing.Mask4D import Mask4D


class PostProcess_Reader : 

    def __init__(self, mask_path, pet_path, type): #pt_path
        self.mask_path = mask_path
        self.pet_path = pet_path
        self.type = type

        self.pet_img = self.read_pet_img()
        self.pet_array = self.get_pet_array()
        self.size_matrix = self.pet_array.shape

        self.mask_object = self.get_mask_object()
        


    def get_mask_object(self):
        if self.type == '3d' :
            return Mask3D(self.mask_path)

        elif self.type == '4d' : 
            return Mask4D(self.mask_path)

        else : 
            raise Exception ('Not a 3D or 4D mask ')
        

    def get_mask_array(self):
        """
        Image to array mask with no threshold 3D or 4D
        """
        return self.mask_object.read_mask_array()

    def read_pet_img(self):
        pt_img = sitk.ReadImage(self.pet_path)
        self.pet_origin = pt_img.GetOrigin()
        self.pet_direction = pt_img.GetDirection()
        self.pet_spacing = pt_img.GetSpacing()
        self.pet_size = pt_img.GetSize()
        return pt_img

    def get_pet_array(self): 
        return sitk.GetArrayFromImage(self.pet_img).transpose()

        
    def get_binary_threshold_mask_array(self, threshold):
        """
        Return a 3d binary threshold mask 
        """
        if self.type == '4d' : 
            return self.mask_object.get_binary_threshold_mask(self.pet_array, threshold)
        elif self.type == '3d' : 
            return self.mask_object.get_binary_threshold_mask()
        else : 
            raise Exception ('not a 3d or 4d mask')


    def get_binary_threshold_mask_img(self, threshold):
        binary_array = self.get_binary_threshold_mask_array(threshold)
        new_mask_img = sitk.GetImageFromArray(binary_array.transpose())
        new_mask_img.SetOrigin(self.pet_origin)
        new_mask_img.SetSpacing(self.pet_spacing)
        new_mask_img.SetDirection(self.pet_direction)
        return new_mask_img 


    def get_mask_img_spacing(self):
        return self.mask_object.get_mask_spacing()

    def get_mask_img_size(self):
        return self.mask_object.get_mask_size()
        
    def get_mask_img_origin(self):
        return self.mask_object.get_mask_origin()

    def get_mask_img_direction(self):
        return self.mask_object.get_mask_direction()
        

    def is_details_same(self):
        spacing = self.get_mask_img_spacing()
        size = self.get_mask_img_size()
        origin = self.get_mask_img_origin()
        direction = self.get_mask_img_direction()
        if (self.pet_spacing != spacing) or (self.pet_origin != origin) or (self.pet_direction != direction) or (self.pet_size != size) : 
            raise Exception ('Not the same spacing, size, origin or direction between mask and pet')

        else : return True 


    def get_labelled_threshold_mask_img(self, binary_img):
        if len(binary_img.GetSize()) != 3 : 
            raise Exception("Not a 3D mask, need to transform into 3D binary mask")
        
        else : 
            labelled_img = sitk.ConnectedComponent(binary_img)
            return labelled_img

    def get_labelled_threshold_mask_array(self, labelled_threshold_img):
        return sitk.GetArrayFromImage(labelled_threshold_img).transpose()

    
    def label_stat_results(self, labelled_threshold_img) :
        results = {} 
        stats = sitk.LabelIntensityStatisticsImageFilter()
        stats.Execute(labelled_threshold_img, self.pet_img)
        number_of_label = stats.GetNumberOfLabels()
        results['number_of_label'] =  number_of_label
        for i in range(1, number_of_label + 1) :
            subresult = {}
            subresult['max'] = stats.GetMaximum(i)
            subresult['mean'] = stats.GetMean(i)
            subresult['median'] = stats.GetMedian(i)
            subresult['variance'] = stats.GetVariance(i)
            subresult['sd'] = stats.GetStandardDeviation(i)
            subresult['number_of_pixel'] = stats.GetNumberOfPixels(i)
            volume_voxel = self.pet_spacing[0] * self.pet_spacing[1] * self.pet_spacing[2] * 10**(-3) #ml
            subresult['volume'] = stats.GetNumberOfPixels(i) * volume_voxel
            subresult['centroid'] = stats.GetCentroid(i)

            results[i] = subresult
        return results

    def label_coordonate(self, labelled_mask, stats_results):
        results = {}
        number_of_label = stats_results['number_of_label']
        for i in range(1, number_of_label + 1) :
            subliste = []
            subliste.append(np.where(labelled_mask == i))
            results[i] = subliste
            
        return results
    