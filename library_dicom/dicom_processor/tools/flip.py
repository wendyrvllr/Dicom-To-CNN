import csv
import numpy as np 
import SimpleITK as sitk 
from library_dicom.dicom_processor.tools.threshold_mask import *


def get_suv_max_value(mask_path, pet_path):
    img_mask = sitk.ReadImage(mask_path)
    img_pet = sitk.ReadImage(pet_path)
    mask_array = sitk.GetArrayFromImage(img_mask).transpose()
    pet_array = sitk.GetArrayFromImage(img_pet).transpose()
    mask_array = get_threshold_matrix_4D(mask_array, pet_array, 0.41 )
    #print(mask_array.shape)
    pixel_spacing = img_pet.GetSpacing() #[x,y,z]
    #print("spacing :", img_pet.GetSpacing())
    #print("mask spacing : ", img_mask.GetSpacing())
    volume_voxel = pixel_spacing[0]*pixel_spacing[1]*pixel_spacing[2] * 10**(-3)

    if len(mask_array.shape) != 3 : 
        number_of_roi = mask_array.shape[3]
    else : 
        number_of_roi = 1

    volume = []

    for i in range(number_of_roi) : 
        if number_of_roi != 1 :
            number_pixel = len(np.where(mask_array[:,:,:,i] == 1)[0])
        else : 
            number_pixel = len(np.where(mask_array == 1)[0])

        volume.append(volume_voxel * number_pixel)

    #print(volume)
    volume_max = np.max(volume)
    roi_max = volume.index(volume_max)

    if number_of_roi != 1 : 
        roi = mask_array[:,:,:,roi_max]

    else : roi = mask_array

    x,y,z = np.where(roi == 1)

    suv_values = []
    for j in range(len(x)):
        suv_values.append(pet_array[x[j],y[j],z[j]])

    return roi_max, np.round(np.max(suv_values), 2)

    

