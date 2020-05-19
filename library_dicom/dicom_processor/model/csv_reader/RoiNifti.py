import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

"""Derivated Class for automatic Nifti ROI of PetCtViewer.org

Returns:
    [RoiNifti] -- Nifti ROI
"""
class RoiNifti(Roi):

    def __init__(self, roi_number, list_point, volume_dimension):
        super().__init__(1, 0, 0, roi_number, 0, list_point, volume_dimension)

    def calculateMaskPoint(self):
        np_array_3D = super().get_empty_np_array()
        #print(np_array_3D.shape) 144 144 255

        pixel_array = self.list_point_np 

        for points in pixel_array :
            
            np_array_3D[points[0], points[1], points[2]] = self.roi_number
        return np.transpose(np_array_3D.astype(np.uint8), (1,0,2))
        #return np_array_3D.astype(np.uint8)