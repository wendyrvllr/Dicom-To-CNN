from library_dicom.dicom_processor.enums.SopClassUID import *
import SimpleITK as sitk
import numpy as np

class NiftiBuilder:
    """BuildNifti File using a Series Object
    """

    def __init__(self, series):
        self.series = series
    
    def save_nifti(self, filename, mask = None):
        if( mask == None) : 
            sitk_img = sitk.GetImageFromArray( np.transpose(self.series.get_numpy_array(), (2,0,1) ))
        else :
            sitk_img = mask
        
        original_pixel_spacing = self.series.instance_array[0].get_pixel_spacing()
        #print(self.series.instance_array[0].get_image_orientation())
        sitk_img.SetDirection( (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0) )
        sitk_img.SetOrigin( self.series.instance_array[0].get_image_position() )
        sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.series.get_z_spacing()) )
        sitk.WriteImage(sitk_img, filename)