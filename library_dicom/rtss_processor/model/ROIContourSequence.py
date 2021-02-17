import pydicom 
import numpy as np
import cv2 
from random import randrange
from library_dicom.dicom_processor.model.reader.Instance_RTSS import Instance_RTSS
from library_dicom.rtss_processor.tools_rtss.switch_modality import *


class ROIContourSequence : 

    def __init__(self, dict_roi_data, mask_4D=None, modal_rtss_path=None, root_origin=None, target_origin=None):
        """[summary]

        Args:
            dict_roi_data ([dict]): [description]
            mask_4D ([ndarray], optional): [4D ndarray/ If we want to write a RTSS from a ndarray mask.]. Defaults to None.
            modal_rtss_path ([str], optional): [RTSS path for new contour by switching modality method]. Defaults to None.
            root_origin ([list], optional): [IF CT to PET : ct origin [x,y,z], ELSE : pet origin]. Defaults to None.
            target_origin ([list], optional): [IF CT to PET : pet origin [x,y,z], ELSE : ct_origin]. Defaults to None.
        """
        if mask_4D is not None : 
            self.mask_4D = mask_4D
            self.number_of_roi = self.mask_4D.shape[3]

        if modal_rtss_path is not None : 
            self.modal_rtss_path = modal_rtss_path
            self.modal_rtss_object = Instance_RTSS(self.modal_rtss_path)
            #self.number_of_roi = self.modal_rtss_object.get_number_of_roi()
            self.root_origin = root_origin 
            self.target_origin = target_origin 

        self.dict_roi_data = dict_roi_data


    def __get_contour_ROI(self, number_roi):
        if self.mask_4D : 
            results = {}
            slice = []

            binary_mask = np.array(self.mask_4D[:,:,:,number_roi - 1], dtype=np.uint8)

            for s in range(self.mask_4D.shape[2]):
                contours, _ = cv2.findContours(binary_mask[:,:, s], cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
                if (contours != []) : 
                    results[s] = contours
                    slice.append(s)

            return results, slice 

        if self.modal_rtss_object : 
            number_of_roi = len(self.dict_roi_data)
            self.number_of_roi = number_of_roi
            index = []
            for i in range(1, self.number_of_roi +1):
                index.append(self.dict_roi_data[i]['ROINumber'])

            contour = []
            for idx in index:
                contour.append(self.modal_rtss_object.get_contour_data(idx))

            #str to float
            for roi in contour : 
                for slice in roi : 
                    for i in range(len(slice)):
                        slice[i] = float(slice[i])

            return contour, _

    def pixel_to_spatial(self, number_roi, image_position, pixel_spacing, list_all_SOPInstanceUID):

        list_contours = []
        list_SOPInstanceUID = []
        x0,y0,z0 = image_position
        dx,dy,dz = pixel_spacing
        dict_contours, list_slice = self.__get_contour_ROI(number_roi)

        number_contour = len(dict_contours)

        for i in range(number_contour): #plusieurs contours dans une même slice 
            number_of_contour_in_slice = len(dict_contours[list_slice[i]])
            for j in range(number_of_contour_in_slice)  : 
                number_point_contour = len(dict_contours[list_slice[i]][j])

                liste = []

                for point in range(number_point_contour): #[x,y]
                    x = dict_contours[list_slice[i]][j][point][0][0]
                    liste.append(x0 + x*dx + dx/2 )
                    y = dict_contours[list_slice[i]][j][point][0][1]
                    liste.append( y0 + y*dy + dy/2)
                    z = list_slice[i] 
                    liste.append(z0 + z*dz )

                list_SOPInstanceUID.append(list_all_SOPInstanceUID[z])
                list_contours.append(liste)

        return list_contours, list_SOPInstanceUID

    def generate_new_contour(self):
        contour, _ = self.__get_contour_ROI(None)
        return switch_modality(contour, self.root_origin, self.target_origin), [] 


    def __create_ContourImageSequence(self, ReferencedSOPClassUID, ReferencedSOPInstanceUID=None):
        ContourImageSequence = pydicom.sequence.Sequence()
        dataset = pydicom.dataset.Dataset()
        dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
        if ReferencedSOPInstanceUID is not None : 
            dataset.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID
        ContourImageSequence.append(dataset)
        return ContourImageSequence 

    def __create_ContourSequence(self, ReferencedSOPClassUID, list_ReferencedSOPInstanceUID, list_ContourData):
        ContourSequence = pydicom.sequence.Sequence()
        if len(list_ReferencedSOPInstanceUID) != 0 :
            for ContourData,SOPInstanceUID in zip(list_ContourData,list_ReferencedSOPInstanceUID):
                dataset = pydicom.dataset.Dataset()
                dataset.ContourData = ContourData 
                dataset.ContourGeometricType = 'CLOSED_PLANAR'
                
                dataset.ContourImageSequence = self.__create_ContourImageSequence(ReferencedSOPClassUID, SOPInstanceUID)
                
                dataset.NumberOfContourPoints = len(ContourData)/3

                ContourSequence.append(dataset)
            return ContourSequence 

        else : 
            for ContourData in list_ContourData:
                dataset = pydicom.dataset.Dataset()
                dataset.ContourData = ContourData 
                dataset.ContourGeometricType = 'CLOSED_PLANAR'
                
                dataset.ContourImageSequence = self.__create_ContourImageSequence(ReferencedSOPClassUID)
                
                dataset.NumberOfContourPoints = len(ContourData)/3

                ContourSequence.append(dataset)
            return ContourSequence 


    @classmethod
    def get_random_colour(cls):
        max = 256
        return [randrange(max), randrange(max), randrange(max)]



    def create_ROIContourSequence(self, ReferencedSOPClassUID, image_position, pixel_spacing, list_all_SOPInstanceUID):
        ROIContourSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ROIDisplayColor = self.get_random_colour()
            dataset.ReferencedROINumber = number_roi
            if self.mask_4D : 
                list_contour_data , list_SOP_instance_uid = self.pixel_to_spatial(number_roi, image_position, pixel_spacing, list_all_SOPInstanceUID)
                dataset.ContourSequence = self.__create_ContourSequence(ReferencedSOPClassUID, list_SOP_instance_uid, list_contour_data)
            if self.modal_rtss_object : 
                list_contour_data, list_SOP_instance_uid = self.generate_new_contour()
                dataset.ContourSequence = self.__create_ContourSequence(ReferencedSOPClassUID, list_SOP_instance_uid, list_contour_data)
            ROIContourSequence.append(dataset)
        return ROIContourSequence 