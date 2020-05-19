#classe pour 1 roi RTSS, stocker les infos d'un roi RTSS
from library_dicom.ROI_Contour import ROI_Contour

#voir class de thomas dans file New_RTSTruct


class ROI_RTSS:
    """data of ROI RTSS
    """
    def __init__(self, origin, filename):
        self.origin = origin #DicomRT or mask 
        self.filename = filename #original filename 
    
    #setteur
    #StructureSetRoiSequence
    def set_number_roi(self, number_roi):
        self.number_roi = number_roi

    def set_name_roi(self, name_roi):
        self.name_roi = name_roi

    def set_referenced_frame_of_reference(self, referenced_frame_of_reference):
        self.referenced_frame_of_reference = referenced_frame_of_reference

    def set_roi_generation_algorithm(self, roi_generation_algorithm):
        self.roi_generation_algorithm = roi_generation_algorithm

    #ROIContourSequence
    def set_contours_roi_sequence(self):
        self.contours_roi_sequence = ROI_Contour()
        #voir comment utiliser objet ROI_contour

    #ReferencedFrameOfReferenceSequence 
    def set_frame_of_reference_UID(self, frame_of_reference_UID):
        self.frame_of_reference_UID = frame_of_reference_UID

    def set_RT_referenced_study_sequence(self, referenced_study_sequence): #sous sequence
        self.referenced_study_sequence = referenced_study_sequence
    #dans RTReferencedStudySequence : 

    def set_referenced_SOP_class_UID(self, referenced_SOP_class_UID):
        self.referenced_SOP_class_UID = referenced_SOP_class_UID

    def set_referenced_SOP_instance_UID(self, referenced_SOP_instance_UID):
        self.referenced_SOP_instance_UID = referenced_SOP_instance_UID
    
    def set_RT_referenced_serie_sequence(self, RT_referenced_serie_sequence): #sous sous  sequence
        self.RT_referenced_serie_sequence = RT_referenced_serie_sequence
    #dans RTReferencedSerieSequence

    def set_series_instance_UID(self, series_instance_UID):
        self.series_instance_UID = series_instance_UID

    def set_contour_image_sequence(self, contour_image_sequence): # sous sous sous sequence
        self.contour_image_sequence = contour_image_sequence
    
    #dans ContourImageSequence
    #a nouveau un ReferencedSOPClassUID et ReferencedSOPInstanceUID différent



    #methode get 