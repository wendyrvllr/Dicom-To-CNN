from library_dicom.dicom_processor.model.Series import Series
import numpy as np

class SeriesCT(Series):
    """Get Series CT Nifti in 16 Bits

    Arguments:
        Series {String} -- Series Location Path
    """

    def __init__(self,path):
        super().__init__(path)

    def get_numpy_array(self):
        numpy_array = super().get_numpy_array()
        return numpy_array.astype(np.int16)

    def export_nifti(self, file_path, mask = None):
        if (mask is None) : 
            
            sitk_img = sitk.GetImageFromArray( np.transpose(self.get_numpy_array(), (2,0,1) ))
            sitk_img = sitk.Cast(sitk_img, sitk.sitkInt16)

            original_pixel_spacing = self.instance_array[0].get_pixel_spacing()
            
            original_direction = self.instance_array[0].get_image_orientation()
            sitk_img.SetDirection( (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]), 
                                    0.0, 0.0, 1.0) )
            sitk_img.SetOrigin( self.instance_array[0].get_image_position() )
            sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.get_z_spacing()) )
            sitk.WriteImage(sitk_img, file_path)

        else : 
            number_of_roi = mask.shape[3] #tjrs de taille 4, si une seule roi=> dernier channel =1
            slices = []
            for number_roi in range(number_of_roi) : 
                slices.append(np.transpose(mask[:,:,:,number_roi], (2,0,1)))
                
            mask_4D = np.stack(slices, axis = 3)
            sitk_img = sitk.GetImageFromArray(mask_4D, isVector = True)
            sitk_img = sitk.Cast(sitk_img, sitk.sitkVectorUInt8)
            
            original_pixel_spacing = self.instance_array[0].get_pixel_spacing()
            original_direction = self.instance_array[0].get_image_orientation()
            sitk_img.SetDirection( (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]), 
                                    0.0, 0.0, 1.0) )
            sitk_img.SetOrigin( self.instance_array[0].get_image_position() )
            sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.get_z_spacing()) )
            sitk.WriteImage(sitk_img, file_path)
