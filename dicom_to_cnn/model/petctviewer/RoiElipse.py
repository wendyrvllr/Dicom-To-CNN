import matplotlib.patches
import numpy as np
import math
from dicom_to_cnn.model.petctviewer.Roi import Roi


class RoiElipse(Roi):
    """Derivated Class for manual Elipse ROI of PetCtViewer.org

    Returns:
        [RoiElipse] -- Roi Elipse Object
    """

    def __init__(self, axis:int, first_slice:int, last_slice:int, roi_number:int, type_number:int, list_point:list, volume_dimension:tuple):
        """constructor

        Args:
            axis (int): [1 for axial, 2 for coronal, 3 for saggital]
            first_slice (int): [slice number where ROI begin]
            last_slice (int): [slice number where ROI end]
            roi_number (int): [roi number]
            type_number (int): [ 11 for axial ellipse, 12 for coronal ellipse, 13 for saggital ellipse]
            list_point (list): [list of [x,y] coordonates of ellipse in CSV]
            volume_dimension (tuple): [(shape x, shape y, shape z)]
        """
        super().__init__(axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension)
        self.list_points = self.calculateMaskPoint()


    def calculateMaskPoint(self):
        """ calculate [x,y,z] coordonates/voxel which belong to the ROI in ellipse patches

        Returns:
            [list]: [list of [x,y,z] coordonates of ROI ]
        """
        points_array = self.list_point_np 
        x0 = points_array[0][0]
        y0 = points_array[0][1]
        delta_x = points_array[1][0] - x0
        delta_y = abs(points_array[2][1] - y0)
        middle = ((self.first_slice + self.last_slice) / 2) - 1
        rad1 = ((self.last_slice - self.first_slice) / 2) 
        list_points = []
        if(rad1 == 0) :
            return list_points
        for number_slice in range(self.first_slice  , self.last_slice - 1 ) : 
            diff0 = abs(middle - number_slice)
            factor = pow(rad1,2) - pow(diff0,2)
            factor = math.sqrt(factor) / rad1
            width = factor * delta_x
            height = factor * delta_y
            roi_pixel_matplot = self.__create_elipse(2 * width, 2 * height)
            point = super().mask_roi_in_slice(roi_pixel_matplot)
            for i in range(len(point)):
                point[i].append(number_slice)
            list_points.extend(point)
        return list_points

    def __create_elipse(self, width:float, height:float) -> matplotlib.patches.Ellipse: 
        """generate an ellipse patches from matplotlib

        Args:
            width (float): [widht of ellipse]
            height (float): [height of ellipse]

        Returns:
            [matplotlib.patches.Ellipse]: [Ellipse patche]
        """
        points_array = self.list_point_np  
        return matplotlib.patches.Ellipse(points_array[0], width, height, angle = 0)



    