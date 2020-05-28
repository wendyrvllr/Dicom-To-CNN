import pydicom

class ROI_Contour(pydicom.dataset.Dataset):

    def __init__(self):
        super().__init__()

    def set_ContourImageSequence(self, ReferencedSOPClassUID, ReferencedSOPInstanceUID):
        self.ContourImage = pydicom.sequence.Sequence()
        dataset = pydicom.dataset.Dataset()
        dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
        dataset.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID
        self.ContourImage.append(dataset)
        return self.ContourImage 

    def set_ContourSequence(self, ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData):
        self.ContourSequence = pydicom.sequence.Sequence()
        for ContourData,SOPInstanceUID in zip(list_ContourData,list_SOPInstanceUID):
            dataset = pydicom.dataset.Dataset()
            dataset.ContourData = ContourData 
            dataset.ContourGeometricType = ContourGeometricType
            # creation of a ContourImageSequence
            dataset.ContourImageSequence = self.set_ContourImageSequence(ReferencedSOPClassUID, SOPInstanceUID)
            
            dataset.NumberOfContourPoints = len(ContourData)/3

            self.ContourSequence.append(dataset)
        return self.ContourSequence 


