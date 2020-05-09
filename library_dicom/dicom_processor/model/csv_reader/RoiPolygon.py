import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

class RoiPolygon(Roi):

    def __init__(self, axis, first_slice, last_slice, roi_number, list_point):
        self.axis = axis
        self.first_slice = first_slice
        self.last_slice = last_slice
        self.roi_number = roi_number
        self.list_point = list_point

    def calculateMaskPoint(self):
        volume_dimension = super().get_volume_dimension()
        np_array_3D = np.zeros((volume_dimension[0], volume_dimension[1], volume_dimension[2]))
        xmin, ymin, xmax, ymax  = Roi.get_min_max_of_roi(np_array_3D)

        roi_pixel_matplot = self.___create_closed_polygon()

        #SK : Pourquoi le +1 ici que dans last slice ?
        for number_of_slices in range(self.first_slice, self.last_slice + 1 ) : 
            np_array_3D[number_of_slices] = Roi.mask_roi_in_slice(xmin, ymin, xmax, ymax, np.zeros(volume_dimension[0], volume_dimension[1]), roi_pixel_matplot, self.roi_number) 
        
        if (self.axis == 2) : 
            np_array_3D = Roi.coronal_to_axial(np_array_3D)
        elif (self.axis == 3) :
            np_array_3D = Roi.sagittal_to_axial(np_array_3D)

        return np_array_3D.astype(np.uint8)

    def ___create_closed_polygon(self):
        points_array = Roi.pointlist_to_pointarray(self.point_list)
        return matplotlib.patches.Polygon(points_array, closed = True)