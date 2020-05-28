from library_dicom.dicom_manipulations import convert_MASK_to_ROI 


class Mask_To_RTSS:
    """build a DicomRT from a Mask 
    """
    def __init__(self, mask): 
        self.mask = mask 


    def get_roi_rtss_from_mask(self, label_numbers, list_SOPInstanceUID, dicom_spacing, dicom_origin):
        list_ROI = []
        list_UID = []

        x0,y0,z0 = dicom_origin
        dx,dy,dz = dicom_spacing

        
    


#1) convert mask to roi rtss
#2) create RTStruct from a mask => fichier .dcm 
 
#code de thomas 
#voir comment on réorganise 


