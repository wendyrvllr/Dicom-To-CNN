import numpy as np
import matplotlib.pyplot as plt

import SimpleITK as sitk 


def read_mask_nifti(mask_path):
    mask_img = sitk.ReadImage(mask_path)
    pixel_spacing = mask_img.GetSpacing()
    origin = mask_img.GetOrigin()
    direction = mask_img.GetDirection()
    size = mask_img.GetSize()

    return pixel_spacing, origin, direction, size


def build_nifti_mask(mask, mask_path, pixel_spacing, origin, direction) : 

    number_of_roi = mask.shape[3]

    slices = []
    for number_roi in range(number_of_roi):

        sitk_img = sitk.GetImageFromArray( np.transpose(mask[:,:,:,number_roi], (2,0,1) ))
        
        if len(direction) == 9 : #mask3D => 1 ROI
            sitk_img.SetDirection( (float(direction[0]), float(direction[1]), float(direction[2]), 
                                    float(direction[3]), float(direction[4]), float(direction[5]), 
                                    float(direction[6]), float(direction[7]), float(direction[8]) ))
        
        
        else : 
            sitk_img.SetDirection( (float(direction[0]), float(direction[1]), float(direction[2]), 
                                    float(direction[4]), float(direction[5]), float(direction[6]), 
                                    float(direction[8]), float(direction[9]), float(direction[10]) ))
        sitk_img.SetOrigin( (origin[0], origin[1], origin[2] ))
        sitk_img.SetSpacing( (pixel_spacing[0], pixel_spacing[1], pixel_spacing[2]) )
        slices.append(sitk_img)
            
    img = sitk.JoinSeries(slices)
    sitk.WriteImage(img, mask_path)
