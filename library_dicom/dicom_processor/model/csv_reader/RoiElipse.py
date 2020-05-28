import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi
import cmath

"""Derivated Class for manual Elipse ROI of PetCtViewer.org

Returns:
    [RoiElipse] -- Roi Elipse Object
"""
class RoiElipse(Roi):

    def __init__(self, axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension):
        super().__init__(axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension)

    def calculateMaskPoint(self):
        np_array_3D = super().get_empty_np_array()
        x,y,z = np_array_3D.shape

        points_array = self.list_point_np - 1 
        x0 = points_array[0][0]
        y0 = points_array[0][1]

        delta_x = points_array[1][0] - x0
        delta_y = abs(points_array[2][1] - y0)
        middle = ((self.first_slice + self.last_slice) / 2) - 1
        
        rad1 = ((self.last_slice - self.first_slice) / 2) - 1 

        list_points = []
        list_slices = []

        for number_of_slices in range(self.first_slice -1 , self.last_slice ) : 
            
            diff0 = abs(middle - number_of_slices)
            
            factor = pow(rad1,2) - pow(diff0,2)
            factor = cmath.sqrt(factor) / rad1

            width = np.real(factor * delta_x)
            height = np.real(factor * delta_y)
            
            roi_pixel_matplot = self.__create_elipse(2* width, 2* height)
            mask, point = super().mask_roi_in_slice(np.zeros( (x,y) ), roi_pixel_matplot, self.roi_number)

            np_array_3D[:,:,number_of_slices] = mask
            list_slices.append(number_of_slices)
            list_points.append(point)
        
    
        if (self.axis == 2) : 
            return  super().coronal_to_axial(np_array_3D)
        elif (self.axis == 3) :
            return super().sagittal_to_axial(np_array_3D)

        return np.transpose(np_array_3D.astype(np.uint8), (1,0,2)) , list_points, list_slices

    def __create_elipse(self, width, height): 
        points_array = self.list_point_np  
        #width = 2 * abs(points_array[0][0] - points_array[1][0]) #centre_x - est_x 
        #height = 2 * abs(points_array[0][1] - points_array[2][1]) #centre_y - nord_y
        return matplotlib.patches.Ellipse(points_array[0], width, height, angle = 0)



    