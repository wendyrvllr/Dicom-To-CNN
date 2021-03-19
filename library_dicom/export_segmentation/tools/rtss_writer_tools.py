import numpy as np 
from skimage.measure import label 

def get_image_position_per_slice(liste_instances):
    liste = []
    for i in range(len(liste_instances)):
        liste.append(liste_instances[i].get_image_position())
    return liste 


def find_corresponding_z_spatial(liste_position, z_matrix):
    z_spatial = liste_position[z_matrix][2]
    return z_spatial


def get_number_of_roi(mask):
    if len(mask.shape) == 3 : 
        if np.max(mask) == 1 : 
            return 1 
        else : return int(np.max(mask))

    elif len(mask.shape) == 4 : 
        if np.max(mask) == 1 : 
            return mask.shape[3]
        else : return int(np.max(mask))


def get_list_SOPInstance_UID(liste_instances):
    liste = []
    for instance in liste_instances : 
        liste.append(instance.get_SOPInstanceUID())

    return liste 


def clean_mask(mask):
    """[summary]

    Args:
        mask ([type]): [binary mask [x,y,z]]
    """
    #Check if binary mask 
    
    if int(np.max(mask)) != 1 :
        raise Exception("Not a binary mask")

    empty_mask = np.zeros((mask.shape))
    for s in range(mask.shape[2]) : 
        slice = mask[:,:,s]
        if int(np.max(slice)) == 0 : 
            empty_mask[:,:,s] = slice
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
            empty_mask[:,:,s] = lw 

    #binarize image 
    matrix = np.where(empty_mask>0, 1, 0)
    return matrix








    