#classe pour 1 roi RTSS, stocker les infos d'un roi RTSS
import pydicom

class ROI_RTSS:
    """data of ROI RTSS
    """
    def __init__(self, origin, filename, number_roi):
        self.origin = origin #DicomRT or mask 
        self.filename = filename #original filename 
        self.number_roi = number_roi #numero de la ROI
    
    #setteur


    def set_ROIDisplayColor(self,ROIDisplayColor): #couleur [255, 0,0] par ex
        self.ROIDisplayColor = ROIDisplayColor

    def set_ContourSequence(self): #OBJET ROI CONTOUR 
        self.ContourSequence = pydicom.sequence.Sequence()

    def set_ReferencedROINumber(self, ReferencedROINumber):
        self.ReferencedROINumber = ReferencedROINumber

    

    def get_ROIDisplayColor(self):
        return self.ROIDisplayColor

    def get_ContourSequence(self):
        return self.ContourSequence

    def get_ReferencedROINumber(self):
        return self.ReferencedROINumber

    