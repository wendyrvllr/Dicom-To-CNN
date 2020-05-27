#classe pour 1 roi RTSS, stocker les infos d'un roi RTSS
import pydicom
from library_dicom.rtss_processor.model.ROI_Contour import ROI_Contour

class ROI_RTSS(pydicom.dataset.Dataset):
    def __init__(self):
        super().__init__()

    def set_ROIContourSequence(self, DisplayColor, list_SliceWithContour, ReferencedSOPClassUID, ReferencedSOPInstanceUID, ContourGeometricType, NumberOfContourPoints, ContourData):
        self.ROIContour = pydicom.dataset.Dataset()
        self.ROIContour.DisplayColor = DisplayColor
        self.ROIContour.ContourSequence = pydicom.sequence.Sequence()
        roi_contour = ROI_Contour()

        self.ROIContour.ContourSequence.append(roi_contour.set_ContourSequence(list_SliceWithContour, ReferencedSOPClassUID, ReferencedSOPInstanceUID, ContourGeometricType, NumberOfContourPoints, ContourData))
    
    def get_ROIContourSequence(self):
        return self.ROIContour 