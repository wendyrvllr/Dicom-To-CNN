import numpy as np

#with any threshold 3d mask label

def threshold_matrix(mask_array, pet_array, threshold):
    """

    mask_array (z,x,y,C)
    pet_array (z,x,y)
    """
    mask_array = mask_array.astype('int8')
    if threshold < 1 : 
        if len(mask_array.shape) != 3 :  #mask 4D 
            number_of_roi = mask_array.shape[3]
            liste = []
            for i in range(number_of_roi):
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] )).astype('uint8')
                suv_values = []
                x,y,z = np.where(mask_array[:,:,:,i] != 0)
                if len(x) != 0 : 
                    suv_values = pet_array[x,y,z].tolist()
                   
                    seuil = np.max(suv_values) * threshold
                    
                    new_mask[np.where((pet_array > seuil) & (mask_array[:,:,:,i] > 0))] = 1
                    
                    liste.append(new_mask.astype('iunt8'))
                    
                else : liste.append(new_mask.astype('uint8'))

            return np.stack(liste, axis = 3).astype('uint8')   

        else : 
            maxi = np.max(mask_array)
            if maxi == 1.0 : 
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] )).astype('uint8')
                x,y,z = np.where(mask_array != 0)
                suv_values = pet_array[x,y,z].tolist()
                seuil = np.max(suv_values) * threshold
                new_mask[np.where((pet_array > seuil) & (mask_array > 0))] = 1
                return new_mask.astype('uint8')
                 

            else :  
                number_of_roi = maxi
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] )).astype('uint8')
                for i in range(number_of_roi):
                    suv_values = []
                    x,y,z = np.where(mask_array == i)
                    suv_values = pet_array[x,y,z].tolist()
                    seuil = np.max(suv_values) * threshold
                    new_mask[np.where((pet_array > seuil) & (mask_array == i))] = i
                return new_mask.astype('uint8')



    else : 
        if len(mask_array.shape) != 3 :  #mask 4D 
            number_of_roi = mask_array.shape[3]
            liste = []
            for i in range(number_of_roi):
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] )).astype('uint8')
                seuil = threshold
                new_mask[np.where((pet_array > seuil) & (mask_array[:,:,:,i] > 0))] = 1
                liste.append(new_mask)

            return np.stack(liste, axis = 3)    

        else : 
            maxi = np.max(mask_array)
            if maxi == 1.0 : 
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                seuil = threshold
                new_mask[np.where((pet_array > seuil) & (mask_array > 0))] = 1
                return new_mask
                 

            else :  
                number_of_roi = maxi
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                seuil = threshold
                for i in range(number_of_roi):
                    new_mask[np.where((pet_array > seuil) & (mask_array == i))] = i
                return new_mask




