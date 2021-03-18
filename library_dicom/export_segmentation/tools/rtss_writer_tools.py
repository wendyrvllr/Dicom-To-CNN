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
        mask ([type]): [labelled mask [x,y,z]]
    """
    #Check if binary mask 
    if len(mask.shape) == 3 : 
        number_of_roi = int(np.max(mask))


        #remove ROI with 1 or 2 pixels 
        new_mask = np.zeros((mask.shape))
        for i in range(1, number_of_roi+1):
            x,y,z = np.where(mask == i)
            if len(x) > 2 : 
                new_mask[x,y,z] = mask[x,y,z]

        #remove slice with 1 or 2 pixel per ROI 
        #binarize matrix
        b = np.where(mask>0,1,0)
        new_mask = b

        new_mask_2 = np.zeros((new_mask.shape))
        for s in range(new_mask.shape[2]):
            x,y = np.where(new_mask[:,:,s] != 0)
            if len(x) > 2 : 
                new_mask_2[:,:,s] = new_mask[:,:,s]

        labelled_array, features = label(new_mask_2, connectivity=2, return_num = True)
        return labelled_array


    elif len(mask.shape) == 4 : 
        if int(np.max(mask)) != 1 : 
            b = np.where(mask>0,1,0)
            mask = b
        
        new_mask = np.zeros((mask.shape))
        for roi in range(mask.shape[3]):
            for s in range(mask.shape[2]):
                x,y = np.where(mask[:,:,s, roi] != 0)
                if len(x) > 2 : 
                    new_mask[:,:,s, roi] = mask[:,:,s, roi]
            return new_mask 



    