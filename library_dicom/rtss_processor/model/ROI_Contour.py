import pydicom

class ROI_Contour(pydicom.dataset.Dataset):

    def __init__(self):
        super().__init__()

    def set_ContourImageSequence(self, ReferencedSOPClassUID, ReferencedSOPInstanceUID):
        self.ContourImage = pydicom.dataset.Dataset()
        self.ContourImage.ReferencedSOPClassUID = ReferencedSOPClassUID
        self.ContourImage.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID
        return self.ContourImage

    def set_ContourSequence(self, list_SliceWithContour, ReferencedSOPClassUID, ReferencedSOPInstanceUID, ContourGeometricType, NumberOfContourPoints, ContourData):
        self.ContourSequence = pydicom.sequence.Sequence()
        for slice in (list_SliceWithContour):
            contour = pydicom.dataset.Dataset()
            contour.ContourImageSequence = pydicom.sequence.Sequence()
            contour.ContourImageSequence.append(self.set_ContourImageSequence(ReferencedSOPClassUID, slice))
            contour.ContourGeometricType = ContourGeometricType
            contour.NumberOfContourPoints = NumberOfContourPoints
            contour.ContourData = ContourData
            self.ContourSequence.append(contour)
        return self.ContourSequence 

