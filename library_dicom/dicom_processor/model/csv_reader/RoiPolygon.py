import matplotlib.patches
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

class RoiPolygon(Roi):

    def __init__(self, axis, first_slice, last_slice, roi_number, list_point, volume_dimension):
        super().__init__(axis, first_slice, last_slice, roi_number, list_point, volume_dimension)

    def calculateMaskPoint(self):
        np_array_3D = super().get_empty_np_array()
        x,y,z = np_array_3D.shape

        roi_pixel_matplot = self.___create_closed_polygon()


        for number_of_slices in range(self.first_slice, self.last_slice + 1 ) : 
            np_array_3D[:,:,number_of_slices] = super().mask_roi_in_slice( np.zeros( (x, y) ), roi_pixel_matplot, self.roi_number) 
        
        if (self.axis == 2) : 
            np_array_3D = super().coronal_to_axial(np_array_3D)
        elif (self.axis == 3) :
            np_array_3D = super().sagittal_to_axial(np_array_3D)

        return np.transpose(np_array_3D.astype(np.uint8), (1,0,2))

    def ___create_closed_polygon(self):
        points_array = self.list_point_np
        return matplotlib.patches.Polygon(points_array, closed = True)