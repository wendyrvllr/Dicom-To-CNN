class Roi():

    def __init(self, axis, first_slice, last_slice, roi_number, list_point):
        super().__init__(axis, first_slice, last_slice, roi_number, list_point)
    
    def set_volume_dimension(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_volume_dimension(self, x, y, z):
        return (self.x, self.y, self.z)

    def pointlist_to_pointarray (self, point_list):
        """Transforms string point into x/y/z point array for matplotlib : [ [x,y,slice] , [x ,y, slice], ...]

        Arguments:
            point_list {[type]} -- [description]

        Returns:
            [array] -- [matplot lib array]
        """
        size = len(point_list)
        points = []
        for i in range(size):
            points.append(point_list[i].split())
        return np.asarray(points)
    
    def get_min_max_of_roi(self, point_list):
        """Compute extrema of ROI in which we will loop to find included voxel

        Arguments:
            point_list {[type]} -- [description]

        Returns:
            [minx, miny, maxx, maxy] -- X/Y extremas
        """
        points_array = Roi.pointlist_to_pointarray(point_list)
        x = []
        y= []
        for i in range (points_array.shape[0]):
            x.append(points_array[i, 0])
            y.append(points_array[i, 1])
        return min(x), min(y), max(x), max(y)

    def mask_roi_in_slice(self,  xmin, ymin, xmax, ymax, sliceToMask, patch, number_of_roi): #patch = ellipse ou polygone #slice = np array 256*256
        for i in range(xmin, xmax): 
            for j in range(ymin, ymax) : 
                if patch.contains_point([i,j], radius = 0) : #si vrai alors changement 
                    sliceToMask[i,j] =  number_of_roi # = 1,2,3 etc 
        return sliceToMask
    
    def get_empty_np_array(self):
        if(self.axis == 1):
            return np.zeros((self.x, self.y, self.z))
        elif (self.axis == 2):
            return np.zeros((self.x, self.z, self.y))
        elif (self.axis == 3):
            return np.zeros((self.y, self.z, self.x))

    def coronal_to_axial(self, np_array_3D):
        return np.transpose(np_array_3D, (1,2,0)) #coronnal x y z -> axial y z x 
        #SK A VERIF

    def sagittal_to_axial(self, np_array_3D):
        return np.transpose(np_array_3D, (2,0,1)) #sagittal x y z - > axial  z x y 
        #SK A VERIF
