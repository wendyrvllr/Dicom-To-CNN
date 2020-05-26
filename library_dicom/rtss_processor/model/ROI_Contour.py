import pydicom

class ROI_Contour : 
    """a class to generate contour of a ROI as an object (for RoiContourSequence)
        / ensemble of contour on instance
    """

    def __init__(self, referenced_roi_number): #numero du ROI
        self.referenced_roi_number = referenced_roi_number


    def set_ContourImageSequence(self):
        self.ContourImageSequence = pydicom.sequence.Sequence()

    #dans ContourImageSequence : ClassUID InstanceUID ->
   
    def set_ReferencedSOPClassUID(self, ReferencedSOPClassUID): #le même pour tout les rois 
        self.ReferencedSOPClassUID = ReferencedSOPClassUID

    def set_ReferencedSOPInstanceUID(self, ReferencedSOPInstanceUID): #UID of the slice 
        self.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID


    

    def set_ContourGeometricType(self, ContourGeometricType):  
        self.ContourGeometricType = ContourGeometricType
    
    def set_NumberOfContourPoints(self, NumberOfContourPoints): 
        self.NumberOfContourPoints = NumberOfContourPoints

    def set_ContourData(self, ContourData):
        self.ContourData = ContourData


#methode get de mes infos pour y accéder r
    def get_ContourImageSequence(self):
        return self.ContourImageSequence
    
    def get_ReferencedSOPClassUID(self):
        return self.ReferencedSOPClassUID

    def get_ReferencedSOPInstanceUID(self):
        return self.ReferencedSOPInstanceUID

    def get_ContourGeometricType(self):
        return self.ContourGeometricType

    def get_NumberOfContourPoints(self):
        return self.NumberOfContourPoints
    
    def get_ContourData(self):
        return self.ContourData