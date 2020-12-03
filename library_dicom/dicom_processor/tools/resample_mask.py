import numpy as np 
import SimpleITK as sitk 

#add other modality for mask 


def resample_mask_nifti(concat_img_path, mask_img_path, target_size, target_spacing, target_direction, target_origin = None):
    concat_img = sitk.ReadImage(concat_img_path)
    mask_img = sitk.ReadImage(mask_img_path)
    target_origin = concat_img.GetOrigin()[0:3]
    if len(mask_img.GetSize()) == 3 : 
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(target_direction)
        transformation.SetOutputOrigin(target_origin)
        transformation.SetOutputSpacing(target_spacing)
        transformation.SetSize(target_size)
        transformation.SetDefaultPixelValue(0.0)
        transformation.SetInterpolator(sitk.sitkNearestNeighbor)
        new_mask_img = transformation.Execute(mask_img)

        return sitk.GetArrayFromImage(new_mask_img)
    
