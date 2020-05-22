from library_dicom.dicom_processor.model.Series import Series
import pydicom
import os
import cv2

class RTSS_Reader:

    def __init(self, rtss_path):
        self.rtss_path = rtss_path
        self.filenames = os.listdir(self.rtss_path)
        self.data = pydicom.dcmread(os.path.join(self.rtss_path, self.filenames[0]))

    #methode pour lire patient name, ID, Sex, BirthDate, etc etc avec Series ? 

    def get_number_of_roi(self):
        return len(self.data.StructureSetROISequence)

    #Boucle sur le nombre de rois 


    #info from ReferencedFrameOfReferenceSequence
    def get_frame_of_reference_UID(self):
        number_serie = len(self.data.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.data[0x30060010][i].FrameOfReferenceUID)

        return liste #les mêmes pour les 2 series 

    def is_frame_of_reference_same(self):
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


    def get_list_all_SOP_Instance_UID(self, series_path):
        series_object = Series(series_path) #celle de la CT 
        return series_object.get_all_SOPInstanceIUD #liste 

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
            liste.append(self.data[0x30060039][roi_number - 1].ContourSequence[i].ContourImageSequence[0].ReferencedSOPInstanceUID)
        return liste 

    #check si la coupe ou il y a le contour est bien dans la liste de toutes les coupes de la série
    def is_referenced_SOP_Instance_UID_in_all_SOP_Instance(self):
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
        
    def get_contour_data(self, roi_number):
        number_item = len(self.data[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.data[0x30060039][roi_number - 1].ContourSequence[i].ContourData)
        return liste #liste d'array 


        

    #représentation spatial => pixel 

    def spatial_to_pixels(self, number_roi, series_path):
        frame_of_reference_UID = self.get_frame_of_reference_UID()
        list_referenced_SOP_class_uid = str(self.get_list_referenced_SOP_Instance_UID(number_roi))
        x=[]
        y=[]
        z=[] #recuperer le numero de la coupe 
        list_contour_data = self.get_contour_data(number_roi) #x y z en mm 
        series_object = Series(series_path) #celle de la CT 
        data = series_object.get_series_details()
        pixel_spacing = data['instance']['PixelSpacing'] #[x,y] strdistance between center of 2 pixels
        #x row spacing in mm
        #y column spacing in mm

        #diviser le x et y de list_contour_data (mm) / pixel spacing x y = pixel 



        



