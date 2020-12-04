import numpy as np 
import SimpleITK as sitk 

#add other modality for mask 

#target_size = (128, 128, 256)
#target_spacing = (4.0, 4.0, 4.0)
#target_direction = (1,0,0,0,1,0,0,0,1)


def resample_mask_nifti(concat_img_path, mask_img_path, target_size, target_spacing, target_direction, target_origin = None):
    concat_img = sitk.ReadImage(concat_img_path)
    mask_img = sitk.ReadImage(mask_img_path)
    if target_origin == None : 
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

        return new_mask_img

    else : #mask 4D => mask 4D
        size = mask_img.GetSize()
        liste = []
        for roi in range(size[3]):
            extract = sitk.ExtractImageFilter()
            extract.setSize([size[0], size[1], size[2], 0])
            extract.setIndex([0,0,0,roi])
            extracted_img = extract.Execute(mask_img)
            transformation = sitk.ResampleImageFilter()
            transformation.SetOutputDirection(target_direction)
            transformation.SetOutputOrigin(target_origin)
            transformation.SetOutputSpacing(target_spacing)
            transformation.SetSize(target_size)
            transformation.SetDefaultPixelValue(0.0)
            transformation.SetInterpolator(sitk.sitkNearestNeighbor)
            new_mask_img = transformation.Execute(extracted_img)
            liste.append(new_mask_img)

        img = sitk.JoinSeries(liste)

        return img
    
