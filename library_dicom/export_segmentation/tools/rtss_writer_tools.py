import numpy as np 

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