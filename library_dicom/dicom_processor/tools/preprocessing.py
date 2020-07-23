#nifti CT => preprocess => new size, spacing

import os 
import SimpleITK as sitk  

target_direction = (1,0,0,0,1,0,0,0,1)
target_shape = (255,128,128) #{z, y ,x}
target_voxel_spacing = (4.8, 4.8, 4.8) #mm

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
    target_shape = (128, 128, shape[2]) 

    spacing = ct_img.GetSpacing()
    target_voxel_spacing = (spacing[0]*4, spacing[1]*4, spacing[2]) #mm
    transformation = sitk.ResampleImageFilter()
    transformation.SetOutputDirection(target_direction)
    transformation.SetOutputSpacing(target_voxel_spacing)
    transformation.SetSize(target_shape)
    transformation.SetOutputOrigin(new_origin)
    transformation.SetInterpolator(sitk.sitkBSpline)

    return transformation.Execute(ct_img)