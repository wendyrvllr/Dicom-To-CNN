import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

class RoiNifti(Roi):

    def __init__(self, roi_number, list_point, volume_dimension):
        super().__init__(1, 0, 0, roi_number, 0, list_point, volume_dimension)

    def calculateMaskPoint(self):
        np_array_3D = super().get_empty_np_array()
        #print(np_array_3D.shape)

        pixel_array = self.list_point_np

        for points in pixel_array :
            np_array_3D[points[0]-1, points[1]-1, points[2]-1] = self.roi_number

        return np.transpose(np_array_3D.astype(np.uint8), (1,0,2))
