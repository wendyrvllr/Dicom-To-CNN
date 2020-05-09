import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

class RoiElipse(Roi):

    def __init__(self, axis, first_slice, last_slice, roi_number, list_point, volume_dimension):
        super().__init__(axis, first_slice, last_slice, roi_number, list_point, volume_dimension)

    def calculateMaskPoint(self):
        volume_dimension = super().get_volume_dimension()
        np_array_3D = super().get_empty_np_array()
        xmin, ymin, xmax, ymax  = super().get_min_max_of_roi(np_array_3D)

        roi_pixel_matplot = self.__create_elipse()

        #SK : Pourquoi le +1 ici que dans last slice ?
        for number_of_slices in range(self.first_slice, self.last_slice + 1 ) : 
            np_array_3D[number_of_slices] = super().mask_roi_in_slice(xmin, ymin, xmax, ymax, np.zeros(volume_dimension[0], volume_dimension[1]), roi_pixel_matplot, self.roi_number) 
        
        if (self.axis == 2) : 
            np_array_3D = super().coronal_to_axial(np_array_3D)
        elif (self.axis == 3) :
            np_array_3D = super().sagittal_to_axial(np_array_3D)

        return np_array_3D.astype(np.uint8)

    def __create_elipse(self):
        points_array = super().pointlist_to_pointarray(self.list_point)
        width = abs(points_array[0][0] - points_array[1][0]) #centre_x - est_x 
        height = abs(points_array[0][1] - points_array[2][1]) #centre_y - nord_y
        return matplotlib.patches.Ellipse(points_array[0], width, height, angle = 0)