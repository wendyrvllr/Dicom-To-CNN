from library_dicom.dicom_processor.model.Series import Series
import pydicom
import os
import cv2 as cv2


import numpy as np 



class RTSS_Reader:

    def __init__(self, rtss_path):
        self.rtss_path = rtss_path
        self.filenames = os.listdir(self.rtss_path)
        self.data = pydicom.dcmread(os.path.join(self.rtss_path, self.filenames[0]))

    #methode pour lire patient name, ID, Sex, BirthDate, etc etc avec Series ? 

    def get_number_of_roi(self):
        return len(self.data.StructureSetROISequence)



    #info from ReferencedFrameOfReferenceSequence
    def get_frame_of_reference_UID(self):
        number_serie = len(self.data.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.data[0x30060010][i].FrameOfReferenceUID)

        return liste #les mêmes pour les 2 series 


    def get_number_of_series(self):
        """return number of series in ReferencedFrameOfReferencedSequence

        Returns:
            [int] -- [description]
        """
        return len(self.data.ReferencedFrameOfReferenceSequence)



    def is_frame_of_reference_same(self):
        """check if frame of reference is the same for the series in ReferencedOfReferencedSequence

        Returns:
            [bool] -- [description]
        """
        frame_of_reference_UID = self.get_frame_of_reference_UID()
        for i in range(len(frame_of_reference_UID)):
            if frame_of_reference_UID[0] != frame_of_reference_UID[i] :
                return False 
        return True 

            
    def get_series_instance_UID(self):
        number_serie = len(self.data.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.data[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID)
        return liste

    def get_SOP_class_UID(self):
        number_serie = len(self.data.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.data[0x30060010][i].RTReferencedStudySequence[0].ReferencedSOPClassUID)
        return liste 
        


    def get_list_all_SOP_Instance_UID(self):
        number_item = len(self.data[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.data[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[i].ReferencedSOPInstanceUID))
        return liste


    #info from StructureSetROISequence
    def get_ROI_name(self, number_roi):
        return self.data[0x30060020][number_roi - 1].ROIName 

    def get_ROI_volume(self, number_roi):
        return self.data[0x30060020][number_roi - 1].ROIVolume 

    def get_ROI_generation_algorithm(self, number_roi):
        return self.data[0x30060020][number_roi - 1].ROIGenerationAlgorithm 

    #info from ROIContourSequence

    def get_roi_display_color(self, number_roi):
        return self.data[0x30060039][number_roi - 1].ROIDisplayColor 


    def get_list_referenced_SOP_Instance_UID(self, roi_number): #la ou il y a les contours
        number_item = len(self.data[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.data[0x30060039][roi_number - 1].ContourSequence[i].ContourImageSequence[0].ReferencedSOPInstanceUID))
        return liste 

    
    def is_referenced_SOP_Instance_UID_in_all_SOP_Instance(self):
        """check if slices in which there are a ROI is in the list of all slices of the serie

        Raises:
            Exception: [description]

        Returns:
            [bool] -- [description]
        """
        all_sop = str(self.get_list_all_SOP_Instance_UID)
        referenced_sop = str(self.get_list_referenced_SOP_Instance_UID)
        for uid in referenced_sop : 
            if uid not in all_sop : 
                raise Exception("SOP Instance UID not in the serie")
        return True 


    def get_number_of_contour_points(self, roi_number):
        number_item = len(self.data[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.data[0x30060039][roi_number - 1].ContourSequence[i].NumberOfContourPoints)
        return liste

    def get_list_contour_geometric_type(self, roi_number):
        number_item = len(self.data[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.data[0x30060039][roi_number - 1].ContourSequence[i].ContourGeometricType)
        return liste

    def is_closed_planar(self, roi_number):
        geometric_type = self.get_list_contour_geometric_type(roi_number)
        for type in geometric_type :
            if type != "CLOSED_PLANAR" : 
                return False
        return True 


    def get_contour_data(self, roi_number):
        number_item = len(self.data[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.data[0x30060039][roi_number - 1].ContourSequence[i].ContourData)
        return liste #liste d'array 

        #les z sont les mêmes pour chaque item (ok puisque 1 item = 1 slice )



    def __spatial_to_pixels(self, matrix_size, number_roi, series_path):
        """Transform contour data in spatial to contour data in pixels

        Arguments:
            number_roi {int} -- [number of roi ]
            series_path {str} -- [path of the series ]
            slice_size{list} -- [size x, y of the slice]

        Returns:
            [dict] -- [{1 : { x : []
                               y : []
                               z : []} , 
                       {2 : { x : []
                               y : []
                               z : []} , ...]
        """
        #frame_of_reference_UID = self.get_frame_of_reference_UID()

        list_referenced_SOP_instance_uid = (self.get_list_referenced_SOP_Instance_UID(number_roi))
        
        list_all_sop_Instance_UID =self.get_list_all_SOP_Instance_UID()
        series_object = Series(series_path) #celle de la CT par ex
        data = series_object.get_series_details()
        series_object.get_numpy_array()
        z_spacing = series_object.get_z_spacing()
        print("z_spacing :", z_spacing)
        pixel_spacing = data['instance']['PixelSpacing'] #[x,y]  distance between center of 2 pixels
        print("pixel spacing : ", pixel_spacing)

        image_position = data['instance']['ImagePosition']
        print("image position :", image_position)  # = [-300 -300 325] coordonée x y z coin supérieur gauche
        #image_position[0] = float(image_position[0]) / float(pixel_spacing[0])
        #image_position[1] = float(image_position[1]) / float(pixel_spacing[1])
        #print("image position :", image_position) # =  [-256 -256 325] 

        self.image_position = image_position
        

        #Image CT dans ImageJ : 512 x 512 (=600 600 mm)

        #Dans Slicer3D
        #-256 ... 0 ... 256
        #.
        #.
        #.
        #0        0 
        #.
        #.
        #.
        #256
        
        list_contour_data = self.get_contour_data(number_roi) #x y z en mm 
        list_pixels = {}

        for contour_data in (list_contour_data):
            number_item = list_contour_data.index(contour_data) #0 1 2 3 ...
            contour_item = {}
            x = contour_data[::3]  #list
            x = [int((i - image_position[0]) / pixel_spacing[0]  ) + 1 for i in x ]

            contour_item['x'] = x
            y = contour_data[1::3] #list

            y = [int((i - image_position[1]) / pixel_spacing[1] ) + 1  for i in y ]
            contour_item['y'] = y
            z = list_referenced_SOP_instance_uid[number_item]
            z = list_all_sop_Instance_UID.index(z) #numero de coupe correspondant
            contour_item['z'] = z
            list_pixels[number_item + 1] = contour_item

        return list_pixels

    #eventuellement en privé
    def get_list_points(self, matrix_size, number_roi, series_path):
        """transform a list of pixels of a ROI to a list nx2 (n points, coordonate (x,y)) for each contour

        Arguments:
            number_roi {[int]} -- [description]
            series_path {[str]} -- [description]

        Returns:
            [list] -- list of (x,y) points and list of z slices in which there is a contour
        """
        pixels = self.__spatial_to_pixels(matrix_size, number_roi, series_path) #dict 
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

  
    def rtss_to_3D_mask(self, number_roi, matrix_size, series_path):
        series_object = Series(series_path) #celle de la CT par ex
        number_of_slices = len(series_object.get_all_SOPInstanceIUD())
        np_array_3D = np.zeros(( matrix_size[0],  matrix_size[1], number_of_slices))
        if self.is_closed_planar(number_roi) == False : raise Exception ("Not CLOSED_PLANAR contour")
        liste_points, slice = self.get_list_points(matrix_size, number_roi, series_path)
        ROI_name = self.get_ROI_name(number_roi)
        print("ROI_name :", ROI_name )
        print("number_roi : ", number_roi)
        print("slice : ", slice)
        
        for item in range(len(slice)):
            #print(slice[item])
            np_array_3D[:,:,slice[item]] = cv2.drawContours(np.float32(np_array_3D[:,:,slice[item]]), [np.asarray(liste_points[item])], -1, (255,0,0), -1)

        return np_array_3D


    def rtss_to_4D_mask(self, matrix_size, series_path, matrix_4D = True):
        series_object = Series(series_path) #celle de la CT par ex
        number_of_slices = len(series_object.get_all_SOPInstanceIUD())
        number_of_roi = self.get_number_of_roi()
        np_array_4D = np.zeros((matrix_size[0], matrix_size[1], number_of_slices, number_of_roi))
        for number_roi in range(1, number_of_roi +1):
            #print(number_roi)
            np_array_4D[:,:,:,number_roi-1] = self.rtss_to_3D_mask(number_roi, matrix_size, series_path)

        return np_array_4D








    

        



