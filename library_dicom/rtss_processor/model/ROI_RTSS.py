#classe pour 1 roi RTSS, stocker les infos d'un roi RTSS
import pydicom
from library_dicom.rtss_processor.model.ROI_Contour import ROI_Contour

class ROI_RTSS(pydicom.dataset.Dataset):
    def __init__(self):
        super().__init__()

    def set_ROIContour(self, DisplayColor, ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData):
        self.ROIContour = pydicom.dataset.Dataset()
        self.ROIContour.DisplayColor = DisplayColor
        roi_contour = ROI_Contour()
        contour_sequence = roi_contour.set_ContourSequence(ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData)
        #print(contour_sequence)
        #print(type(contour_sequence))
        self.ROIContour.ContourSequence = contour_sequence
    
        return self.ROIContour 
    