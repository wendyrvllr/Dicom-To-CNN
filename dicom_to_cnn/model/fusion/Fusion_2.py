import numpy as np 
import SimpleITK as sitk 
import os

#target_size = (128, 128, 256)
#target_spacing = (4.0, 4.0, 4.0)
#target_direction = (1,0,0,0,1,0,0,0,1)


class Fusion : 

    def __init__(self):
        pass 

    def set_origin_image(self, origin_img:sitk.Image) -> None : 
        """method to set the origin sitk.Image on which we want to resample 

        Args:
            origin_img (sitk.Image): []
        """
        self.origin_img = origin_img 
        self.origin_size = origin_img.GetSize()
        self.origin_spacing = origin_img.GetSpacing()
        self.origin_direction = origin_img.GetDirection()
        self.origin_origin = origin_img.GetOrigin()

    def set_target_volume(self, target_size: tuple, target_spacing: tuple, target_direction:tuple) -> None : 
        """method to set the target size, spacing and direction 

        Args:
            target_size (tuple): [(x,y,z)]
            target_spacing (tuple): [(x,y,z)]
            target_direction (tuple): [(x,x,x,y,y,y,z,z,z)]
        """
        self.target_size = target_size 
        self.target_spacing = target_spacing 
        self.target_direction = target_direction 

    def __compute_new_origin_head2hips(self) -> None :
        """method to compute new_origin from head

        Returns:
            [tuple]: [return new origin]
        """
        origin_origin = np.asarray(self.origin_origin)
        origin_size = np.asarray(self.origin_size)
        origin_spacing = np.asarray(self.origin_spacing)
        new_origin = (origin_origin[0] + 0.5 * origin_size[0] * origin_spacing[0] - 0.5 * self.target_size[0] * self.target_spacing[0],
                      origin_origin[1] + 0.5 * origin_size[1] * origin_spacing[1] - 0.5 * self.target_size[1] * self.target_spacing[1],
                      origin_origin[2] + 1.0 * origin_size[2] * origin_spacing[2] - 1.0 * self.target_size[2] * self.target_spacing[2])
        return new_origin 
        
    def resample(self, image_to_resample:sitk.Image, defaultValuePixel:float) -> sitk.Image:
        """method to resample a sitk.Image with defined size, target, spacing and origin

        Args:
            image_to_resample (sitk.Image): [shape (x,y,z)]
            defaultValuePixel (float): [Set the pixel value when a transformed pixel is outside of the image, pet and mask =0.0, ct = -1000.0]

        Returns:
            sitk.Image: [return the resampled sitk.Image]
        """
        target_origin = self.__compute_new_origin_head2hips()
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(target_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(defaultValuePixel)
        transformation.SetInterpolator(sitk.sitkLinear)
        resampled_img = transformation.Execute(image_to_resample)
        return resampled_img 




    
