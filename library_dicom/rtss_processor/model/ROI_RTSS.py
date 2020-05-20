#classe pour 1 roi RTSS, stocker les infos d'un roi RTSS
from library_dicom.rtss_processor.model.ROI_Contour import ROI_Contour

#dans un ROI RTSS : StructureSetRoiSequence + RoiContourSequence 


class ROI_RTSS:
    """data of ROI RTSS
    """
    def __init__(self, origin, filename, number_roi):
        self.origin = origin #DicomRT or mask 
        self.filename = filename #original filename 
        self.number_roi = number_roi #numero de la ROI
    
    #setteur
    #StructureSetRoiSequence

    def set_name_roi(self, name_roi):
        self.name_roi = name_roi

    def set_referenced_frame_of_reference_UID(self, referenced_frame_of_reference_UID):
        self.referenced_frame_of_reference_UID = referenced_frame_of_reference_UID

    def set_roi_generation_algorithm(self, roi_generation_algorithm):
        self.roi_generation_algorithm = roi_generation_algorithm

    #ROIContourSequence
    def set_contours_roi_sequence(self, ROI_Contour): #objet Roi_Contour 
        #=> pour un ROI, donne les coupes ou il y va avoir les contours 
         self.contours_roi_sequence = ROI_Contour(self.number_roi)




    def get_number_roi(self):
        return self.number_roi
    def get_name_roi(self):
        return self.name_roi
    def get_referenced_frame_of_referenceuUID(self):
        return self.referenced_frame_of_reference_UID
    def get_roi_generation_algorithm(self):
        return self.roi_generation_algorithm

    def get_contours_roi_objet(self):
        return self.contours_roi_sequence




    