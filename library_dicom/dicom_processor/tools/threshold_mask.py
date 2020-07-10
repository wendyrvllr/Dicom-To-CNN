import numpy as np

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



            
       

            

            