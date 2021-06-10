import matplotlib.patches
from dicom_to_cnn.model.petctviewer.Roi import Roi


class RoiPolygon(Roi):
    """Derivated Class for manual Polygon ROI of PetCtViewer.org

    Returns:
        [RoiPolygon] -- Polygone ROI
    """

    def __init__(self, axis:int, first_slice:int, last_slice:int, roi_number:int, type_number:int, list_point:list, volume_dimension:tuple):
        """constructor

        Args:
            axis (int): [1 for axial, 2 for coronal, 3 for saggital]
            first_slice (int): [slice number where ROI begin]
            last_slice (int): [slice number where ROI end]
            roi_number (int): [roi number]
            type_number (int): [ 1 for axial polygone, 2 for coronal polygone, 3 for saggital polygone]
            list_point (list): [list of [x,y] coordonates of polygon in CSV]
            volume_dimension (tuple): [(shape x, shape y, shape z)]
        """
        super().__init__(axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension)
        self.list_points = self.calculateMaskPoint()

    def calculateMaskPoint(self) -> list:
        """  calculate [x,y,z] coordonates/voxel which belong to the ROI in polygon patches

        Returns:
            [list]: [list of [x,y,z] coordonates of ROI]
        """
        roi_pixel_matplot = self.__create_closed_polygon()
        list_points = []
        for number_slice in range(self.first_slice - 1  , self.last_slice ) : 
            point = super().mask_roi_in_slice(roi_pixel_matplot)
            for i in range(len(point)):
                point[i].append(number_slice) 
            list_points.extend(point)
        return list_points

    def __create_closed_polygon(self) -> matplotlib.patches.Polygon:
        """generate an polygon patches from matplotlib

        Returns:
            [matplotlib.patches.Polygon]: [Polygon patche]
        """
        points_array = self.list_point_np
        return matplotlib.patches.Polygon(points_array, closed = True)