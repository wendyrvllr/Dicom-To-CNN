import numpy as np

class Roi():

    def __init__(self, axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension):
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
        
    
    def __get_min_max_of_roi(self):
        """Compute extrema of ROI in which we will loop to find included voxel

        Arguments:
            point_list {np array} -- numpy point list

        Returns:
            [minx, miny, maxx, maxy] -- X/Y extremas
        """
        points_array = self.list_point_np

        all_x = points_array[:][:,0]
        all_y = points_array[:][:,1]

        if (self.type_number == 1 or self.type_number == 2 or self.type_number == 3) : #si polygone


            xmin = min(all_x)
            xmax = max(all_x)
            ymin = min(all_y)
            ymax = max(all_y)
        
            return xmin , xmax , ymin , ymax 
        else : #ellipse
            height =  abs(all_x[0] - all_x[1])
            width = abs(all_y[0] - all_y[2])
            xmin = all_x[0] - height
            xmax = all_x[0] + height
            ymin = all_y[0] -  width
            ymax = all_y[0] + width 
            return xmin , xmax , ymin, ymax


    def mask_roi_in_slice(self, patch): #patch = ellipse ou polygone #slice = np array 256*256
        #get Roi limits in wich we will loop
        points = []
        xmin, xmax, ymin, ymax  = self.__get_min_max_of_roi()

        for x in range(xmin-1, xmax + 1): 
            for y in range(ymin-1, ymax + 1) : 
                if patch.contains_point([x,y]) : #radius = 0 
                    points.append([x,y])

        return points
    
    def get_empty_np_array(self):
        """Return numpy array to fill given the current dimension and axis

        Returns:
            numpy array -- zero filled numpy array
        """
        if (self.axis == 1):
            return (np.zeros((self.x, self.y, self.z)))
            
        elif (self.axis == 2):
            return (np.zeros((self.z, self.y, self.x)))

        elif (self.axis == 3):
            return (np.zeros((self.y, self.z, self.x)))

    def coronal_to_axial(self, np_array_3D):
        return np.transpose(np_array_3D, (2,1,0))

        #return np.transpose(np_array_3D, (0,2,1)) #coronnal x y z -> axial z y x 
        #SK A VERIF

    def sagittal_to_axial(self, np_array_3D):
        return np.transpose(np_array_3D, (0,2,1))
        #return np.transpose(np_array_3D, (1,2,0)) #sagittal x y z - > axial y z x 
        #SK A VERIF

    def get_mask(self, list_points, number_roi): #list_points = [[x,y,z], [x,y,z], ...]
        np_array_3D = self.get_empty_np_array()
        for point in list_points:
            np_array_3D[point[0], point[1] ,point[2]] = number_roi

        if (self.axis == 2) : 
            return self.coronal_to_axial(np_array_3D)
        elif (self.axis == 3) :
            return self.sagittal_to_axial(np_array_3D)

        return np.transpose(np_array_3D.astype(np.uint8), (1,0,2))



    

        
    






