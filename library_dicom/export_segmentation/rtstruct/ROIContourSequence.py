import pydicom 
import numpy as np
import cv2 
from random import randrange
from library_dicom.dicom_processor.model.reader.Instance_RTSS import Instance_RTSS
from library_dicom.export_segmentation.tools.rtss_writer_tools import *
from skimage.measure import label, find_contours
import matplotlib.pyplot as plt 
import SimpleITK as sitk 

class ROIContourSequence : 

    def __init__(self, mask_array, mask_img, number_of_roi):
        self.mask_array = mask_array 
        self.mask_img = mask_img
        self.number_of_roi = number_of_roi


    def __define_contour_img(self, number_roi):
        roi = np.zeros((self.mask_array.shape), dtype=np.uint8)
        z,x,y = np.where(self.mask_array == number_roi)
        roi[z,x,y] = 1
        roi_img = sitk.GetImageFromArray(roi)

        return roi_img 
        """
        depth = roi_img.GetDepth()
        contours = []
        for i in range(depth):
            im = roi_img[:,:,i]
            contour = sitk.BinaryContour(im, fullyConnected=True )
            contours.append(contour)
        vectorOfImages = sitk.VectorOfImage()
        for contour in contours:
            vectorOfImages.push_back(contour)
        img = sitk.JoinSeries(vectorOfImages)
        return img 
        """



    def get_spatial_coordonate(self, number_roi, list_all_SOPInstanceUID):
        img_roi = self.__define_contour_img(number_roi)
        depth = img_roi.GetDepth()
        results = []
        list_SOPInstance = []
        for z in range(depth):
            img_slice = img_roi[:,:,z]
            array_slice = sitk.GetArrayFromImage(img_slice)
            #liste = []
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

    """
    def __get_contour_ROI(self, number_roi):

        results = {}
        slice = []
        if self.mask.shape[-1] != 1 : 
            binary_mask = np.array(self.mask[:,:,:,number_roi - 1], dtype=np.uint8)
        else : 
            binary_mask = np.zeros((self.mask.shape[0], self.mask.shape[1], self.mask.shape[2]))
            x,y,z = np.where(self.mask[:,:,:,0] == number_roi)
            binary_mask[x,y,z] = 1
            binary_mask = np.array(binary_mask, dtype=np.uint8 )

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
            for j in range(number_of_contour_in_slice):
                number_point_contour = len(dict_contours[list_slice[i]][j])

                liste = []

                for point in range(number_point_contour): #[x,y]
                    x = dict_contours[list_slice[i]][j][point][0][0]
                    liste.append(x0 + x*dx) #+dx/2
                    y = dict_contours[list_slice[i]][j][point][0][1]
                    liste.append( y0 + y*dy) #+dy/2
                    z = list_slice[i] 
                    z_spatial = find_corresponding_z_spatial(liste_position, z)
                    #liste.append(z0 + z*dz )
                    liste.append(z_spatial) 


                list_SOPInstanceUID.append(list_all_SOPInstanceUID[z])
                list_contours.append(liste)


        return list_contours, list_SOPInstanceUID
    """

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
            dataset.NumberOfContourPoints = len(ContourData)/3 
            dataset.ContourGeometricType = 'CLOSED_PLANAR'

            ContourSequence.append(dataset)
        return ContourSequence 


    @classmethod
    def get_random_colour(cls):
        max = 256
        return [randrange(max), randrange(max), randrange(max)]


    def create_ROIContourSequence(self, ReferencedSOPClassUID, list_all_SOPInstanceUID, liste_instances):
        ROIContourSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            #print("number_roi :", number_roi)
            dataset = pydicom.dataset.Dataset()
            dataset.ROIDisplayColor = self.get_random_colour()
            dataset.ReferencedROINumber = number_roi
            #list_contour_data , list_SOP_instance_uid = self.pixel_to_spatial(number_roi, image_position, pixel_spacing, list_all_SOPInstanceUID, liste_instances)
            list_contour_data, list_SOP_instance_uid = self.get_spatial_coordonate(number_roi, list_all_SOPInstanceUID )
            dataset.ContourSequence = self.__create_ContourSequence(ReferencedSOPClassUID, list_SOP_instance_uid, list_contour_data)
            ROIContourSequence.append(dataset)
        return ROIContourSequence 


