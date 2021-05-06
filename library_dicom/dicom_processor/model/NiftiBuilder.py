from library_dicom.dicom_processor.enums.SopClassUID import *
import SimpleITK as sitk
import numpy as np

class NiftiBuilder:
    """BuildNifti File using a Series Object
    """

    def __init__(self, series):
        self.series = series

    
    def save_nifti(self, filename, mode = 'pet', mask = None):
        if( mask is None) : 
            sitk_img = sitk.GetImageFromArray( np.transpose(self.series.get_numpy_array(), (2,0,1) ))
            if mode == 'pet' : 
                
                sitk_img = sitk.Cast(sitk_img, sitk.sitkFloat32)
            else : #ct
                
                sitk_img = sitk.Cast(sitk_img, sitk.sitkInt16)
            original_pixel_spacing = self.series.instance_array[0].get_pixel_spacing()
            
            original_direction = self.series.instance_array[0].get_image_orientation()
            sitk_img.SetDirection( (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]), 
                                    0.0, 0.0, 1.0) )
            sitk_img.SetOrigin( self.series.instance_array[0].get_image_position() )
            sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.series.get_z_spacing()) )
            #print(sitk_img.GetMetaData('bitpix'))
            #sitk_img.SetMetaData('bitpix', '32')
            
            #print(sitk_img.GetMetaData('bitpix'))
            
            #sitk_img.SetMetaData('datatype', '32')

            sitk.WriteImage(sitk_img, filename)
            
            
            
        else :
            
            number_of_roi = mask.shape[3]
            slices = []
            for number_roi in range(number_of_roi):

                sitk_img = sitk.GetImageFromArray( np.transpose(mask[:,:,:,number_roi], (2,0,1) ))
                #print('3d')
                sitk_img = sitk.Cast(sitk_img, sitk.sitkUInt8)
        
                original_pixel_spacing = self.series.instance_array[0].get_pixel_spacing()
                original_direction = self.series.instance_array[0].get_image_orientation()
                sitk_img.SetDirection( (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]), 
                                    0.0, 0.0, 1.0) )
                sitk_img.SetOrigin( self.series.instance_array[0].get_image_position() )
                sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.series.get_z_spacing()) )
                slices.append(sitk_img)
            
            img = sitk.JoinSeries(slices)
            #img = sitk.Cast(img, sitk.sitkUInt32)
            #print('4d')
            sitk.WriteImage(img, filename)

