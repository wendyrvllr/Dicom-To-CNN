from library_dicom.dicom_processor.enums.SopClassUID import *
import SimpleITK as sitk

class NiftiBuilder:
    """BuildNifi using a Series Object
    """

    def __init__(self, series, filename):
        self.series = series
    
    def __prepare_value(self):
        if(series.sop_class_uid == ImageModalitiesSOPClass.PT or series.sop_class_uid == ImageModalitiesSOPClass.EnhancedPT ) :
            self.__calculate_suv_factor()
        else: self.save_nifti()
    
    def __calculate_suv_factor(self):
        return 1
    
    def save_nifti(self):
        sitk_img = sitk.GetImageFromArray( self.series.get_numpy_array() )
        sitk_img.SetDirection( self.series.instance_array[0].get_image_orientation() )
        sitk_img.SetOrigin( self.series.instance_array[0].get_image_position() )
        sitk_img.SetSpacing( self.series.instance_array[0].get_pixel_spacing() )
        sitk.WriteImage(sitk_img, self.filename)