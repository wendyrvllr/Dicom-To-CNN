import numpy as np
import SimpleITK as sitk 
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage import segmentation
from library_dicom.post_processing.PostProcess_Reader import PostProcess_Reader

class WatershedModel_v2(PostProcess_Reader):

    def __init__(self, mask_path, pet_path, type):
        super().__init__(mask_path, pet_path, type)
    

    
    #def get_number_of_localMax(self, localMax):
        #return len(localMax)

    def watershed_segmentation(self, pet_array, binary_mask_array) : 
        pet_values = np.zeros(self.size_matrix)
        pet_values[np.where(binary_mask_array == 1)] = pet_array[np.where(binary_mask_array == 1)]
        D = ndimage.distance_transform_edt(pet_values)
        localMax2 = peak_local_max(D, indices = False, min_distance= 5)
        structure = np.ones((3,3,3))
        markers, num_features = ndimage.label(localMax2, structure=structure)

        ws_array = segmentation.watershed(-D, markers, mask=pet_values)

        return ws_array.astype(np.uint8), num_features


    def rois_details(self, ws_array, number_of_label) : 
        dic = {}
        vol_tot = 0
        volume_voxel = self.pet_spacing[0] * self.pet_spacing[1] * self.pet_spacing[2] * 10**(-3)
        for i in range(1, number_of_label + 1) : 
            number_pixel = len(np.where(ws_array == i)[0])
            dic[i] = volume_voxel * number_pixel
            vol_tot += volume_voxel * number_pixel

        dic['vol_tot'] = vol_tot

        return dic 