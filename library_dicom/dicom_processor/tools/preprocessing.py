#nifti CT => preprocess => new size, spacing

import os 
import SimpleITK as sitk  


def read_nifti_ct(ct_path):
    return sitk.ReadImage(ct_path)



def normalize_CT(ct_img):
    intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
    #intensityWindowingFilter.SetOutputMaximum(1)
    #intensityWindowingFilter.SetOutputMinimum(0)
    windowMax = 1024
    windowMin = -1024
    intensityWindowingFilter.SetWindowMaximum(windowMax)
    intensityWindowingFilter.SetWindowMinimum(windowMin)
    return intensityWindowingFilter.Execute(ct_img)


def resample_CT(ct_img, new_origin):
        # transformation parametrisation
    target_direction = (1,0,0,0,1,0,0,0,1)
    shape = ct_img.GetSize()
    target_shape = (128, 128, 255) 
    factor_z = shape[2] / target_shape[2]
    factor_x_y = shape[0] / target_shape[0]
    spacing = ct_img.GetSpacing()
    target_voxel_spacing = (spacing[0]*factor_x_y, spacing[1]*factor_x_y, spacing[2] * factor_z) #mm
    transformation = sitk.ResampleImageFilter()
    transformation.SetOutputDirection(target_direction)
    transformation.SetOutputSpacing(target_voxel_spacing)
    transformation.SetSize(target_shape)
    transformation.SetOutputOrigin(new_origin)
    transformation.SetInterpolator(sitk.sitkBSpline)

    return transformation.Execute(ct_img)