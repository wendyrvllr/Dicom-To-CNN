import numpy as np

#with any threshold 3d mask label

def get_threshold_matrix(ws_array, pet_array, number_of_roi, threshold) : #0.41
    for i in range(1, number_of_roi + 1):
        points = []
        suv_values = []
        x,y,z = np.where(ws_array == i)
        for j in range(len(x)): 
            points.append([x[j], y[j], z[j]])

        for point in points : 
            suv_values.append(pet_array[point[0], point[1], point[2]])

        seuil = np.max(suv_values) * threshold

        for point in points : 
            if pet_array[point[0], point[1], point[2]] <= seuil : 
                ws_array[point[0], point[1], point[2]] = 0

    return ws_array

#for 4D matrix
def get_threshold_matrix_4D(mask, pet_array, number_of_roi, threshold) : #0.41
    for i in range(number_of_roi):
        suv_max = []
        x,y,z = np.where(mask[:,:,:,i] != 0)
        for j in range(len(x)):
            suv_max.append(pet_array[x[j], y[j], z[j]])


        seuil = threshold * np.max(suv_max)

        a,b,c = np.where(pet_array <= seuil)
        for k in range(len(x)) :
            mask[a[k], b[k], c[k], i] = 0
        
    return mask


#from csv

def get_suv_max(nifti_array, list_points):
    list_suv = []
    if list_points != [] :
        for point in list_points : 
            list_suv.append(nifti_array[point[1], point[0], point[2]])

        return np.max(list_suv)
    else : return 0.0 #pas de suv max


def threshold_mask(mask_4D, details_rois, nifti_array):

    number_of_roi = mask_4D.shape[3]

    for roi in range(number_of_roi) : 
        list_points = details_rois[roi + 1]['list_points']
        suv_max = get_suv_max(nifti_array, list_points)

            #GET THRESHOLD
        threshold = details_rois['SUVlo']
        if "%" in threshold : 
            threshold = float(threshold.strip("%"))/100 * suv_max
        else : 
            threshold = float(threshold)
        

        for point in list_points :
            if nifti_array[point[1], point[0], point[2]] <= threshold :

                mask_4D[point[1], point[0], point[2], roi] = 0
 
    return mask_4D



            
       

            

            