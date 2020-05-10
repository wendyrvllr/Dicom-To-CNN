import numpy as np

class Roi():

    def __init__(self, axis, first_slice, last_slice, roi_number, list_point, volume_dimension):
        self.axis = axis
        self.first_slice = first_slice
        self.last_slice = last_slice
        self.roi_number = roi_number
        self.list_point = list_point
        self.list_point_np = np.asarray(self.list_point)
        self.x = volume_dimension[0]
        self.y = volume_dimension[1]
        self.z = volume_dimension[2]
        
    
    def __get_min_max_of_roi(self):
        """Compute extrema of ROI in which we will loop to find included voxel

        Arguments:
            point_list {np array} -- numpy point list

        Returns:
            [minx, miny, maxx, maxy] -- X/Y extremas
        """
        points_array = self.list_point_np

        all_x = points_array[:][:,0]
        all_y =points_array[:][:,1]

        xmin = min(all_x)
        xmax = max(all_x)
        ymin = min(all_y)
        ymax = max(all_y)
        
        return xmin, xmax, ymin, ymax

    def mask_roi_in_slice(self, sliceToMask, patch, number_of_roi): #patch = ellipse ou polygone #slice = np array 256*256
        #get Roi limits in wich we will loop
        xmin, ymin, xmax, ymax  = self.__get_min_max_of_roi()
        for i in range(xmin, xmax): 
            for j in range(ymin, ymax) : 
                if patch.contains_point([i,j], radius = 0) : #si vrai alors changement 
                    sliceToMask[i,j] =  number_of_roi # = 1,2,3 etc 
        return sliceToMask
    
    def get_empty_np_array(self):
        """Return numpy array to fill given the current dimension and axis

        Returns:
            numpy array -- zero filled numpy array
        """
        if(self.axis == 1):
            return np.zeros((self.x, self.y, self.z))
        elif (self.axis == 2):
            return np.zeros((self.x, self.z, self.y))
        elif (self.axis == 3):
            return np.zeros((self.y, self.z, self.x))

    def coronal_to_axial(self, np_array_3D):
        return np.transpose(np_array_3D, (0,2,1)) #coronnal x y z -> axial x z y
        #SK A VERIF

    def sagittal_to_axial(self, np_array_3D):
        return np.transpose(np_array_3D, (1,2,0)) #sagittal x y z - > axial y z x 
        #SK A VERIF
