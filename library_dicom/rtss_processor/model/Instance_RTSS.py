from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.model.Instance import Instance
import pydicom
import os
import cv2 as cv2
import numpy as np 
import sys 



class Instance_RTSS(Instance):
    """Class to read dicom RT file and build mask 
    """

    def __init__(self, rtss, serie_path):
        super().__init__(rtss, load_image=True)
        serie = Series(serie_path)
        self.serie_data = serie.get_series_details()
        self.instance_uid_serie = serie.get_all_SOPInstanceIUD()
        self.matrix_size = serie.get_size_matrix()
        #self.rtss_path = rtss_path
        #self.filenames = os.listdir(self.rtss_path)
        #self.data = pydicom.dcmread(os.path.join(self.rtss_path, self.filenames[0]))

    def get_image_nparray(self):
        sys.exit('Cannot get image numpy array from RTSTRUCT FILE')



    def get_list_all_SOP_Instance_UID_serie(self):
        return self.instance_uid_serie


    def get_list_all_SOP_Instance_UID_RTSS(self):
        number_item = len(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[i].ReferencedSOPInstanceUID))
        
        return liste

    def is_sop_instance_uid_same(self):
        uid_serie = self.get_list_all_SOP_Instance_UID_serie()
        uid_rtss = self.get_list_all_SOP_Instance_UID_RTSS()
        for uid in uid_rtss : 
            if uid not in uid_serie : 
                return False

        return True 




    def get_image_position(self):
        return self.serie_data['instance']['ImagePosition']

    def get_pixel_spacing(self):
        return self.serie_data['instance']['PixelSpacing']



    def get_number_of_roi(self):
        return len(self.dicomData.StructureSetROISequence)



    #info from ReferencedFrameOfReferenceSequence
    def get_number_of_referenced_series(self):
        """return number of series in ReferencedFrameOfReferencedSequence

        """
        return len(self.dicomData.ReferencedFrameOfReferenceSequence)


    def get_frame_of_reference_uid(self):
        #Doit etre le meme que FrameOfReferenceUID de la serie CT/PT
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].FrameOfReferenceUID)

        return liste #les mêmes pour les 2 series 



    def is_frame_of_reference_same(self):
        """check if frame of reference is the same for the series in ReferencedOfReferencedSequence

        """
        frame_of_reference_UID = self.get_frame_of_reference_uid()
        for i in range(len(frame_of_reference_UID)):
            if frame_of_reference_UID[0] != frame_of_reference_UID[i] :
                return False 
        return True 


    def get_referenced_series_instance_uid(self):
        #doit être le même que SeriesInstanceUID de la CT/PT
        """get series instance UID from the CT/PT serie 


        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID)
        return liste


    def get_referenced_study_SOP_instance_uid(self):
        #Doit etre le meme que la StudyInstanceUID de la CT/PT
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].ReferencedSOPInstanceUID)
        return liste


    def get_referenced_SOP_class_UID(self):
        #Doit etre le meme que SOPClassUID de la serie CT/PT
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[0].ReferencedSOPClassUID)
        return liste 

 
    #info from StructureSetROISequence
    def get_ROI_name(self, number_roi):
        return self.dicomData[0x30060020][number_roi - 1].ROIName 

    def get_ROI_volume(self, number_roi):
        return self.dicomData[0x30060020][number_roi - 1].ROIVolume 

    def get_ROI_generation_algorithm(self, number_roi):
        return self.dicomData[0x30060020][number_roi - 1].ROIGenerationAlgorithm 

    #info from ROIContourSequence

    def get_roi_display_color(self, number_roi):
        return self.dicomData[0x30060039][number_roi - 1].ROIDisplayColor 


    def get_list_referenced_SOP_Instance_UID(self, roi_number): #la ou il y a les contours
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourImageSequence[0].ReferencedSOPInstanceUID))
        return liste 

    
    def is_referenced_SOP_Instance_UID_in_all_SOP_Instance(self):
        """check if slices in which there is a ROI is in the list of all slices of the serie

        """
        all_sop = str(self.get_list_all_SOP_Instance_UID_RTSS)
        referenced_sop = str(self.get_list_referenced_SOP_Instance_UID)
        for uid in referenced_sop : 
            if uid not in all_sop : 
                raise Exception("SOP Instance UID not in the serie")
        return True 


    def get_number_of_contour_points(self, roi_number):
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].NumberOfContourPoints)
        return liste

    def get_list_contour_geometric_type(self, roi_number):
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourGeometricType)
        return liste

    def is_closed_planar(self, roi_number):
        geometric_type = self.get_list_contour_geometric_type(roi_number)
        for type in geometric_type :
            if type != "CLOSED_PLANAR" : 
                return False
        return True 


    def get_contour_data(self, roi_number):
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourData)
        return liste #liste d'array 




    def __spatial_to_pixels(self, matrix_size, number_roi, list_all_SOPInstanceUID):
        """Transform contour data in spatial to contour data in pixels, return a dict 


        Returns:
            [dict] -- [{1 : { x : []
                               y : []
                               z : []} , 
                       {2 : { x : []
                               y : []
                               z : []} , ...]
        """
        #frame_of_reference_UID = self.get_frame_of_reference_UID()

        pixel_spacing = self.get_pixel_spacing()
        image_position = self.get_image_position()

        list_referenced_SOP_instance_uid = self.get_list_referenced_SOP_Instance_UID(number_roi)
        
        list_contour_data = self.get_contour_data(number_roi) #x y z en mm 
        list_pixels = {}

        for contour_data in (list_contour_data):
            number_item = list_contour_data.index(contour_data) #0 1 2 3 ...
            contour_item = {}
            x = contour_data[::3]  #list
            x = [int((i - image_position[0]) / pixel_spacing[0] ) for i in x ] 

            contour_item['x'] = x
            y = contour_data[1::3] #list
            y = [int((i - image_position[1]) / pixel_spacing[1] )  for i in y ] 
            contour_item['y'] = y
            z = list_referenced_SOP_instance_uid[number_item]
            z = list_all_SOPInstanceUID.index(z) #numero de coupe correspondant
            contour_item['z'] = z
            list_pixels[number_item + 1] = contour_item

        return list_pixels

    #eventuellement en privé
    def get_list_points(self, matrix_size, number_roi, list_all_SOPInstanceUID):
        """transform a list of pixels of a ROI to a list nx2 (n points, coordonate (x,y)) for each contour

        Arguments:
            number_roi {[int]} -- [description]
            series_path {[str]} -- [description]

        Returns:
            [list] -- list of (x,y) points and list of z slices in which there is a contour
        """
        pixels = self.__spatial_to_pixels(matrix_size, number_roi, list_all_SOPInstanceUID) #dict 
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

  
    def rtss_to_3D_mask(self, number_roi, matrix_size, list_all_SOPInstanceUID):
        number_of_slices = matrix_size[2]
        np_array_3D = np.zeros(( matrix_size[0],  matrix_size[1], number_of_slices)).astype(np.uint8)
        if self.is_closed_planar(number_roi) == False : raise Exception ("Not CLOSED_PLANAR contour")
        liste_points, slice = self.get_list_points(matrix_size, number_roi, list_all_SOPInstanceUID )

        for item in range(len(slice)):
            #print(slice[item])
            np_array_3D[:,:,slice[item]] = cv2.drawContours(np.float32(np_array_3D[:,:,slice[item]]), [np.asarray(liste_points[item])], -1, number_roi , -1)

        return np_array_3D


    def rtss_to_4D_mask(self):
        matrix_size = self.matrix_size
        list_all_SOPInstanceUID = self.get_list_all_SOP_Instance_UID_RTSS()
        number_of_roi = self.get_number_of_roi()
        
        np_array_3D = []
        for number_roi in range(1, number_of_roi +1):
            np_array_3D.append(self.rtss_to_3D_mask(number_roi, matrix_size, list_all_SOPInstanceUID))
        np_array_4D = np.stack((np_array_3D), axis = 3)

        return np_array_4D








    

        



