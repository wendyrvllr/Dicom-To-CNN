import numpy as np
import matplotlib.patches 

class Roi():
    """A class to represent a ROI
    """

    def __init__(self, axis:int, first_slice:int, last_slice:int, roi_number:int, type_number:int, list_point:list, volume_dimension:tuple):
        """constructor

        Args:
            axis (int): [1 for axial, 2 for coronal, 3 for saggital]
            first_slice (int): [slice number where ROI begin]
            last_slice (int): [slice number where ROI end]
            roi_number (int): [roi number]
            type_number (int): [0 for nifti, 1 for axial polygone, 11 for axial ellipse, 2 for coronal polygone, 12 for coronal ellipse, 3 for saggital polygone, 13 for saggital ellipse]
            list_point (list): [list of [x,y] coordonates of polygone or ellipse / list of [x,y,z] coordonates of nifti]
            volume_dimension (tuple): [(shape x, shape y, shape z)]
        """
        self.axis = axis
        self.first_slice = first_slice
        self.last_slice = last_slice
        self.roi_number = roi_number
        self.type_number = type_number
        self.list_point = list_point
        self.list_point_np = np.asarray(self.list_point)
        self.x = volume_dimension[0]
        self.y = volume_dimension[1]
        self.z = volume_dimension[2]
        
    
    def __get_min_max_of_roi(self) -> tuple:
        """Compute extrema of ROI in which we will loop to find included voxel

        Arguments:
            point_list {np.ndarray} -- numpy point list

        Returns:
            [tuple] -- X/Y extremas
        """
        points_array = self.list_point_np
        all_x = points_array[:][:,0]
        all_y = points_array[:][:,1]
        if (self.type_number == 1 or self.type_number == 2 or self.type_number == 3) : #POLYGONE
            xmin = min(all_x)
            xmax = max(all_x)
            ymin = min(all_y)
            ymax = max(all_y)
            return xmin , xmax , ymin , ymax 
        else : #ELLIPSE
            height =  abs(all_x[0] - all_x[1])
            width = abs(all_y[0] - all_y[2])
            xmin = all_x[0] - height
            xmax = all_x[0] + height
            ymin = all_y[0] -  width
            ymax = all_y[0] + width 
            return xmin , xmax , ymin, ymax


    def mask_roi_in_slice(self, patch:matplotlib.patches) -> list:
        """get ROI x and y limits in which we will loop, to gather [x,y] pixel which are in the patch

        Args:
            patch (matplotlib.patches): [polygon or ellipse]]

        Returns:
            [list]: [list of [x,y] coordonates]
        """
        points = []
        xmin, xmax, ymin, ymax  = self.__get_min_max_of_roi()
        for x in range(xmin, xmax + 1): 
            for y in range(ymin, ymax + 1) : 
                if patch.contains_point([x,y], radius = -1e-9) : 
                    points.append([x,y])

        return points
    
    def get_empty_np_array(self) -> np.ndarray:
        """Return numpy array to fill given the current dimension and axis

        Returns:
            [np.ndarray] -- zero filled numpy array
        """
        return (np.zeros((self.x, self.y, self.z)))

    def coronal_to_axial(self, np_array_3D:np.ndarray) -> np.ndarray:
        """transform coronal 3d ndarray to 3d axial ndarray

        Args:
            np_array_3D (np.ndarray): [ROI ndarray]]

        Returns:
            [np.ndarray]: [return axial ndarray]
        """
        return np.transpose(np_array_3D, (2,1,0))

    def sagittal_to_axial(self, np_array_3D:np.ndarray) -> np.ndarray:
        """transform saggital 3d ndarray to 3d axial ndarray

        Args:
            np_array_3D (np.ndarray): [ROI ndarray]]

        Returns:
            [np.ndarray]: [return axial ndarray]
        """
        return np.transpose(np_array_3D, (0,2,1))

    def get_mask(self, list_points:list) -> np.ndarray : #list_points = [[x,y,z], [x,y,z], ...]
        """generate an empty ndarray and fill up with ROI coordonates

        Args:
            list_points (list): [ [[x,y,z], [x,y,z], [x,y,z], ...] ]

        Returns:
            [np.ndarray]: [return binary ndarray of the ROI]
        """
        np_array_3D = self.get_empty_np_array()
        for point in list_points:
            np_array_3D[point[1], point[0] , point[2]] = 1
        return np_array_3D.astype(np.uint8)



    

        
    






