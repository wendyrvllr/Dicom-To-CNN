from dicom_to_cnn.model.reader.Series import Series
from dicom_to_cnn.model.reader.Instance_RTSS import Instance_RTSS
import cv2 as cv2
import numpy as np 

class MaskBuilder_RTSS : 
    """a class to build an ndarray mask from a RTSS File 
    """

    def __init__(self, rtss_path:str, serie_path:str):
        """constructor

        Args:
            rtss_path (str): [file path of RTSTRUCT dicom file]
            serie_path (str): [directory path of associated serie]
        """

        self.serie = Series(serie_path)
        self.serie.get_instances_ordered()
        self.serie_data = self.serie.get_series_details()
        self.instance_uid_serie = self.serie.get_all_SOPInstanceIUD()
        self.matrix_size = self.serie.get_size_matrix() #[x,y,z] from associated serie
        self.instances = self.serie.get_instances_ordered()
        self.image_position = self.instances[0].get_image_position()
        self.pixel_spacing = self.instances[0].get_pixel_spacing()
        self.pixel_spacing.append(self.serie.get_z_spacing())

        self.rtss = Instance_RTSS(rtss_path)
        self.number_of_roi = self.rtss.get_number_of_roi()


    def is_sop_instance_uid_same(self) -> bool:
        """check if every SOPInstanceUID from RTSTRUCT correspond to SOPINstanceUID from associated serie

        Returns:
            [bool]: [description]
        """
        uid_rtss = self.rtss.get_list_all_SOP_Instance_UID_RTSS()
        for uid in uid_rtss : 
            if uid not in self.instance_uid_serie : 
                return False

        return True

    def __spatial_to_pixels(self, number_roi:int) -> dict:
        """Transform spatial contour data to matrix coordonate contour

        Arguments :
            number_roi [(int)]: [a ROI number, start at 1]

        Returns:
            [dict] -- [{(roi)1 : { x : []
                               y : []
                               z : []} , 
                       {(roi)2 : { x : []
                               y : []
                               z : []} , ...]
        """
        
        list_contour_data = self.rtss.get_contour_data(number_roi) #x y z en mm 
        list_pixels = {}
        for i in range(3):
            self.image_position[i] = float(self.image_position[i])

        for contour_data in (list_contour_data):
            number_item = list_contour_data.index(contour_data) #0 1 2 3 ...
            contour_item = {}
            x = contour_data[::3]  #list
            x = [int(round((i - self.image_position[0]) / self.pixel_spacing[0] )) for i in x ] 
            contour_item['x'] = x
            y = contour_data[1::3] #list
            y = [int(round((i - self.image_position[1]) / self.pixel_spacing[1] ))  for i in y ]
            contour_item['y'] = y
            z = contour_data[2::3]
            z = [int(round((i - self.image_position[2]) / abs(self.pixel_spacing[2]) )) for i in z ][0]
            contour_item['z'] = z
            list_pixels[number_item + 1] = contour_item
        return list_pixels

    def get_list_points(self, number_roi:int) -> list:
        """transform a list of pixels of a ROI to a list nx2 (n points, coordonate (x,y)) for each contour and list of corresponding z slices

        Arguments:
            number_roi ([int]): [a ROI number, start at 1]
          

        Returns:
            [list] -- list of (x,y) points and list of corresponding z slices (in which there is a contour)
        """
        pixels = self.__spatial_to_pixels(number_roi) #dict 
        number_item = len(pixels)
        list_points = []
        slice = []
        for item in range(number_item):
            subliste = []
            list_x = (pixels[item + 1]['x'])
            list_y = (pixels[item + 1]['y'])
            for x,y in zip(list_x, list_y):
                subliste.append([x,y])

            list_points.append(subliste)

            slice.append(pixels[item + 1]['z'])
        return list_points, slice 
    

    def rtss_to_3D_mask(self, number_roi:int, matrix_size:list) -> np.ndarray:
        """method to generate 3D segmentation mask per ROI number

        Args:
            number_roi (int): [a ROI number, start at 1]
            matrix_size (list): [[shape x, shape y, shape z]]

        Raises:
            Exception: [raise Exception if one contour is not CLOSED_PLANAR ]

        Returns:
            [ndarray]: [return 3d ndarray of a ROI]
        """
        number_of_slices = matrix_size[2]
        np_array_3D = np.zeros(( matrix_size[0],  matrix_size[1], number_of_slices)).astype(np.uint8)
        if self.rtss.is_closed_planar(number_roi) == False : raise Exception ("Not CLOSED_PLANAR contour")
        liste_points, slice = self.get_list_points(number_roi)
        for item in range(len(slice)):
            np_array_3D[:,:,slice[item]] = cv2.drawContours(np.float32(np_array_3D[:,:,slice[item]]), [np.asarray(liste_points[item])], -1, number_roi , -1)
        return np_array_3D.astype(np.uint8)


    def rtss_to_4D_mask(self) -> np.ndarray:
        """method to generate 3d ndarray for each ROI, and stack them in a 4D ndarray

        Returns:
            [ndarray]: [return 4d ndarray of mask segmentation]
        """
        matrix_size = self.matrix_size
        np_array_3D = []
        for number_roi in range(1, self.number_of_roi +1):
            np_array_3D.append(self.rtss_to_3D_mask(number_roi, matrix_size))
        np_array_4D = np.stack((np_array_3D), axis = 3)
        return np_array_4D.astype(np.uint8)