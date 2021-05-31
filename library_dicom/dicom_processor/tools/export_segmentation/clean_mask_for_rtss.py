import numpy as np 
from skimage.measure import label 
import SimpleITK as sitk 

""" functions to help build RTSTRUCT file from ndarray
"""


def clean_mask(mask:np.ndarray):
    """a function to clean mask : remove pixel (=1) when there is less than 3 pixels (=1) in slice

    Args:
        mask (np.ndarray): [mask of shape [z,x,y]]

    Raises:
        Exception: [Check if binary mask as argument]

    Returns:
        [ndarray]: [return the cleaned mask in shape [z,x,y]]
    """
    #Check if binary mask 
    
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

    #binarize image 
    matrix = np.where(empty_mask>0, 1, 0)
    return matrix








    