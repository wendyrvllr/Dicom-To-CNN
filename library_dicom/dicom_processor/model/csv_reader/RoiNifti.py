import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

class RoiNifti(Roi):

    def __init__(self, roi_number, list_point, volume_dimension):
        super().__init__(0, 0, 0, roi_number, list_point, volume_dimension)

    def calculateMaskPoint(self):
        volume_dimension = super().get_volume_dimension()
        np_array_3D = np.zeros((volume_dimension[0], volume_dimension[1], volume_dimension[2]))

        pixel_array = super().pointlist_to_pointarray(self.list_point)

        for points in pixel_array :
            np_array_3D[points[2]][points[0], points[1]] = self.roi_number

        return np_array_3D.astype(np.uint8)