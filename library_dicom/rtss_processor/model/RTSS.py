from library_dicom.rtss_processor.model.ROI_RTSS import ROI_RTSS
from library_dicom.dicom_processor.model.Series import Series

class RTSS:
    """A class for DICOM RT format
    """
    
    def __init(self, filename, origin):
        self.filename = filename
        self.origin = origin
        
    def set_series_instance_uid(self, series_instance_uid): #UID des séries ou il y a les ROIS
        self.series_instance_uid = series_instance_uid #serie CT ou PT 

    def set_SOP_class_UID(self, SOP_class_UID): #SOP Class UID de la série 
        self.SOP_class_UID = SOP_class_UID

    def set_list_SOP_instance_UID(self, list_SOP_instance_UID):
        self.list_SOP_instance_UID = list_SOP_instance_UID #list of every instance UID in a serie 


    #RTROIObservationSequence : aucune infos utiles ? 

    def set_roi_contour_sequence(self, roi_number, ROI_RTSS): #ROI RTSS objet
        #=> faire un set pour chaque ROI ? 
        self.roi_contour_sequence = ROI_RTSS(self.origin, self.filename, roi_number)
   
    

    def get_series_instance_uid(self):
        return self.series_instance_uid
    def get_SOP_class_UID(self):
        return self.SOP_class_UID
    def get_list_SOP_instance_UID(self):
        return self.list_SOP_instance_UID
    def get_roi_contour_sequence(self):
        return self.roi_contour_sequence

    def get_metadata(self, series_path): #patient name, sex, ID, etc 
        serie_objet = Series(series_path)
        return serie_objet.get_series_details() 