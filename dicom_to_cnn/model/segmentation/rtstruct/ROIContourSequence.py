import pydicom 
import numpy as np
from random import randrange
from skimage.measure import label, find_contours
import SimpleITK as sitk 

class ROIContourSequence : 
    """a class to represente ROIContourSequence in RTSTRUCT file
    """

    def __init__(self, mask_array:np.ndarray, mask_img:sitk.Image, number_of_roi:int):
        """constructor

        Args:
            mask_array (np.ndarray]): [mask ndarray]
            mask_img ([sitk.Image]): [mask sitk image]
            number_of_roi ([int]): [total number of roi ]
        """
        self.mask_array = mask_array 
        self.mask_img = mask_img
        self.number_of_roi = number_of_roi


    def __define_contour_img(self, number_roi:int) -> sitk.Image :
        """method to extract mask img per ROI number

        Args:
            number_roi (int): [A roi number, start at 1]

        Returns:
            [sitk.Image]: [mask img of ROI number 'number_roi']
        """
        roi = np.zeros((self.mask_array.shape), dtype=np.uint8)
        z,x,y = np.where(self.mask_array == number_roi)
        roi[z,x,y] = 1
        roi_img = sitk.GetImageFromArray(roi)
        return roi_img 


    def get_spatial_coordonate(self, number_roi:int, list_all_SOPInstanceUID:list) -> tuple:
        """Per ROI number, gather spatial coordonates per slices (when there is a contour)
        Args:
            number_roi (int): [a ROI number, start at 1]
            list_all_SOPInstanceUID (list): [list of every SOPInstanceUID from associated dicom serie]

        Returns:
            [tuple]: [list of spatial coordonates [ [contour 1 : [x, y, z, x, y, z...] ], [contour 2 : [x, y, z, x, y, z...]], ... ] and list of SOPInstanceUID [SOPInstanceUID_contour1, SOPINStanceUID_contour2, ...]

        """
        img_roi = self.__define_contour_img(number_roi)
        depth = img_roi.GetDepth()
        results = []
        list_SOPInstance = []
        for z in range(depth):
            img_slice = img_roi[:,:,z]
            array_slice = sitk.GetArrayFromImage(img_slice)
            contour = find_contours(array_slice, level = 0.0)
            if contour != []: 
                for i in range(len(contour)):
                    liste = []
                    l = contour[i].tolist()
                    for item in l:
                        spatial_coord = self.mask_img.TransformIndexToPhysicalPoint([int(item[1]), int(item[0]), int(z)])
                        liste.append(spatial_coord[0])
                        liste.append(spatial_coord[1])
                        liste.append(spatial_coord[2])

                    results.append(liste)
                    list_SOPInstance.append(list_all_SOPInstanceUID[z])

        return results, list_SOPInstance 

    

    def __create_ContourImageSequence(self, ReferencedSOPClassUID:str, ReferencedSOPInstanceUID:str) -> pydicom.Sequence:
        """method to generate ContourImageSequence from ROIContourSequence 

        Args:
            ReferencedSOPClassUID (str): [Referenced SOP Class UID value from associated serie]
            ReferencedSOPInstanceUID (str): [Reference SOPInstance UID value from associated serie]

        Returns:
            [pydicom.Sequence]: [return ContourImageSequence]
        """
        ContourImageSequence = pydicom.sequence.Sequence()
        dataset = pydicom.dataset.Dataset()
        dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
        dataset.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID
        ContourImageSequence.append(dataset)
        return ContourImageSequence 

    def __create_ContourSequence(self, ReferencedSOPClassUID:str, list_ReferencedSOPInstanceUID:list, list_ContourData:list) -> pydicom.Sequence:
        """method to generate ContourSequence from ROIContourSequence

        Args:
            ReferencedSOPClassUID (str): [Referenced SOP Class UID value from associated serie]
            list_ReferencedSOPInstanceUID (list): [list of every SOPInstanceUID (in which we find contour), same size as list_ContourData]
            list_ContourData (list): [list of every ContourData [[x,y,z,x,y,z], [x,y,z,...], ...], same size as list_ReferencedSOPInstanceUID]


        Returns:
            [pydicom.Sequence]: [return ContourSequence]
        """
        ContourSequence = pydicom.sequence.Sequence()

        for ContourData,SOPInstanceUID in zip(list_ContourData,list_ReferencedSOPInstanceUID):
            dataset = pydicom.dataset.Dataset()
            dataset.ContourData = ContourData             
            dataset.ContourImageSequence = self.__create_ContourImageSequence(ReferencedSOPClassUID, SOPInstanceUID)             
            dataset.NumberOfContourPoints = len(ContourData)/3 
            dataset.ContourGeometricType = 'CLOSED_PLANAR'

            ContourSequence.append(dataset)
        return ContourSequence 


    @classmethod
    def get_random_colour(cls) -> list:
        """a class method to generate random color for ROI

        Returns:
            [list]: [return color [r,g,b]]
        """
        max = 256
        return [randrange(max), randrange(max), randrange(max)]


    def create_ROIContourSequence(self, ReferencedSOPClassUID:str, list_all_SOPInstanceUID:list) -> pydicom.Sequence:
        """method to generate ROIContourSequence from RTSTRUCT file 

        Args:
            ReferencedSOPClassUID (str): [ReferencedSOPClass UID value from associated serie]
            list_all_SOPInstanceUID (list): [list of every SOPInstanceUID of each instance from associated dicom serie]

        Returns:
            [pydicom.Sequence]: [return ROIContourSequence]
        """

        ROIContourSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ROIDisplayColor = self.get_random_colour()
            dataset.ReferencedROINumber = number_roi
            list_contour_data, list_SOP_instance_uid = self.get_spatial_coordonate(number_roi, list_all_SOPInstanceUID )
            dataset.ContourSequence = self.__create_ContourSequence(ReferencedSOPClassUID, list_SOP_instance_uid, list_contour_data)
            ROIContourSequence.append(dataset)
        return ROIContourSequence 


