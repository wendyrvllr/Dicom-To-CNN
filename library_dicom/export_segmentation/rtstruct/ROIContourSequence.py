import pydicom 
import numpy as np
import cv2 
from random import randrange
from library_dicom.dicom_processor.model.reader.Instance_RTSS import Instance_RTSS
from library_dicom.export_segmentation.tools.rtss_writer_tools import *

class ROIContourSequence : 

    def __init__(self, mask):
        self.mask = mask
        self.number_of_roi = get_number_of_roi(self.mask)


    def __get_contour_ROI(self, number_roi):

        results = {}
        slice = []

        binary_mask = np.array(self.mask[:,:,:,number_roi - 1], dtype=np.uint8)

        for s in range(self.mask.shape[2]):
            contours, _ = cv2.findContours(binary_mask[:,:, s], cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
            if (contours != []) : 
                results[s] = contours
                slice.append(s)

        return results, slice 


    def pixel_to_spatial(self, number_roi, image_position, pixel_spacing, list_all_SOPInstanceUID, liste_instances):
        liste_position = get_image_position_per_slice(liste_instances)


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
                    z_spatial = find_corresponding_z_spatial(liste_position, z)
                    #liste.append(z0 + z*dz )
                    liste.append(z_spatial)

                list_SOPInstanceUID.append(list_all_SOPInstanceUID[z])
                list_contours.append(liste)

        return list_contours, list_SOPInstanceUID


    def __create_ContourImageSequence(self, ReferencedSOPClassUID, ReferencedSOPInstanceUID):
        ContourImageSequence = pydicom.sequence.Sequence()
        dataset = pydicom.dataset.Dataset()
        dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
        dataset.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID
        ContourImageSequence.append(dataset)
        return ContourImageSequence 

    def __create_ContourSequence(self, ReferencedSOPClassUID, list_ReferencedSOPInstanceUID, list_ContourData):
        ContourSequence = pydicom.sequence.Sequence()

        for ContourData,SOPInstanceUID in zip(list_ContourData,list_ReferencedSOPInstanceUID):
            dataset = pydicom.dataset.Dataset()
            dataset.ContourData = ContourData             
            dataset.ContourImageSequence = self.__create_ContourImageSequence(ReferencedSOPClassUID, SOPInstanceUID)            
            number_of_points = len(ContourData)/3 
            dataset.NumberOfContourPoints = len(ContourData)/3 
            if number_of_points == 1 : 
                dataset.ContourGeometricType = 'POINT'
            else : 
                dataset.ContourGeometricType = 'CLOSED_PLANAR'

            ContourSequence.append(dataset)
        return ContourSequence 


    @classmethod
    def get_random_colour(cls):
        max = 256
        return [randrange(max), randrange(max), randrange(max)]


    def create_ROIContourSequence(self, ReferencedSOPClassUID, image_position, pixel_spacing, list_all_SOPInstanceUID, liste_instances):
        ROIContourSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ROIDisplayColor = self.get_random_colour()
            dataset.ReferencedROINumber = number_roi
            list_contour_data , list_SOP_instance_uid = self.pixel_to_spatial(number_roi, image_position, pixel_spacing, list_all_SOPInstanceUID, liste_instances)
            dataset.ContourSequence = self.__create_ContourSequence(ReferencedSOPClassUID, list_SOP_instance_uid, list_contour_data)
            ROIContourSequence.append(dataset)
        return ROIContourSequence 


