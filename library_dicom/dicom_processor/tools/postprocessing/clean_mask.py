import numpy as np 
from skimage.measure import label 
import SimpleITK as sitk 

""" functions to clean segmentation mask 
"""


def clean_mask(mask:np.ndarray):
    """a function to clean mask : remove pixel (=1) when there is less than 3 pixels (=1) in slice

    Args:
        mask (np.ndarray): [mask of shape [z,y,x]]

    Raises:
        Exception: [Check if binary mask as argument]

    Returns:
        [ndarray]: [return the cleaned binary mask in shape [z,y,x]]
    """
    if int(np.max(mask)) != 1 :
        raise Exception("Not a binary mask")

    empty_mask = np.zeros((mask.shape))
    for s in range(mask.shape[0]) : 
        slice = mask[s, :, :]
        if int(np.max(slice)) == 0 : 
            empty_mask[s, :, :] = slice
        else : 
            lw, num = label(slice, connectivity=2, return_num=True) #lw = 2D slice 
            item = np.arange(1, num+1).tolist()
            area = []
            for it in item : 
                area.append(len(np.where(lw== it)[0]))
            for ar in area : 
                feature = area.index(ar) + 1 
                if int(ar) < 3 : 
                    x,y = np.where(lw == feature)
                    lw[x,y] = 0 
            empty_mask[s, :, :] = lw 

    matrix = np.where(empty_mask>0, 1, 0)
    return matrix



def remove_small_roi(binary_img:sitk.Image, pet_img:sitk.Image):
    """function to remove ROI under 30 ml on a binary sitk.Image

    Args:
        binary_img (sitk.Image): [sitk.Image of size (z,y,x)]
        pet_img (sitk.Image): [sitk.Image of the PET, size (z,y,x)]

    Raises:
        Exception: [raise Exception if not a 3D binary mask]

    Returns:
        [sitk.Image]: [Return cleaned image]
    """

    binary_array = sitk.GetArrayFromImage(binary_img)
    if len(binary_array.shape) != 3 or int(np.max(binary_array)) != 1 : 
        raise Exception("Not a 3D binary mask, need to transform into 3D binary mask")
    else : 
        pet_spacing = pet_img.GetSpacing()
        pet_origin = pet_img.GetOrigin()
        pet_direction = pet_img.GetDirection()
        labelled_img = sitk.ConnectedComponent(binary_img)
        stats = sitk.LabelIntensityStatisticsImageFilter()
        stats.Execute(labelled_img, pet_img)
        labelled_array = sitk.GetArrayFromImage(labelled_img).transpose()
        number_of_label = stats.GetNumberOfLabels()
        volume_voxel = pet_spacing[0] * pet_spacing[1] * pet_spacing[2] * 10**(-3) #in ml 
        for i in range(1, number_of_label + 1) :
            volume_roi = stats.GetNumberOfPixels(i) * volume_voxel
            if volume_roi < float(30) : 
                x,y,z = np.where(labelled_array == i)
                for j in range(len(x)):
                    labelled_array[x[j], y[j], z[j]] = 0
        new_binary_array = np.zeros((labelled_array.shape))
        new_binary_array[np.where(labelled_array != 0)] = 1
        new_binary_img = sitk.GetImageFromArray(new_binary_array.transpose().astype(np.uint8))
        new_binary_img.SetOrigin(pet_origin)
        new_binary_img.SetSpacing(pet_spacing)
        new_binary_img.SetDirection(pet_direction)
        return new_binary_img
        

    