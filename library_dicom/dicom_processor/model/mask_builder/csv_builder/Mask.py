import numpy as np 
import SimpleITK as sitk 


class Mask: 
    """A class to generate mask nifti 
    """

    def __init__(self, mask_array, serie_pet_object):
        """constructor

        Args:
            mask_array ([ndarray]): [mask ndarray]
            serie_pet_object ([SeriesPT]): [SeriesPT object]
        """
        self.mask_array = mask_array 
        self.serie_pet_object = serie_pet_object 


    def export_nifti(self, file_path):
        instance_array = self.serie_pet_object.get_instances_ordered()
        number_of_roi = self.mask_array.shape[3] #tjrs de taille 4, si une seule roi=> dernier channel =1
        slices = []
        for number_roi in range(number_of_roi) : 
            slices.append(np.transpose(self.mask_array[:,:,:,number_roi], (2,0,1)))
                
        mask_4D = np.stack(slices, axis = 3)
        sitk_img = sitk.GetImageFromArray(mask_4D, isVector = True)
        sitk_img = sitk.Cast(sitk_img, sitk.sitkVectorUInt8)
            
        original_pixel_spacing = instance_array[0].get_pixel_spacing()
        original_direction = instance_array[0].get_image_orientation()
        sitk_img.SetDirection( (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]), 
                                    0.0, 0.0, 1.0) )
        sitk_img.SetOrigin( instance_array[0].get_image_position())
        sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.serie_pet_object.get_z_spacing()) )
        sitk.WriteImage(sitk_img, file_path)