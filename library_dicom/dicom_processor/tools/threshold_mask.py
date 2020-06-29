import numpy as np

def get_suv_max(nifti_array, list_points, flip = False):
    list_suv = []
    if list_points != [] :
        for point in list_points : 
            if flip == False : 
                list_suv.append(nifti_array[point[1], point[0], point[2]])

            else : list_suv.append(nifti_array[point[1], point[0], (slice- 1) - point[2]])

        return np.max(list_suv)
    else : return 0.0 #pas de suv max




def threshold_mask(mask_4D, details_rois, nifti_array,  flip = False):
    number_of_roi = mask_4D.shape[3]

    slice = mask_4D.shape[2]
    if flip == False : 
        for roi in range(number_of_roi) : 
            list_points = details_rois[roi + 1]['list_points']
            suv_max = get_suv_max(nifti_array, list_points, flip = False)

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

    else :  
        for roi in number_of_roi : 
            list_points = details_rois[roi + 1]['list_points']
            suv_max = get_suv_max(nifti_array, list_points, flip = True)

            #GET THRESHOLD
            threshold = details_rois['SUVlo']
            if "%" in threshold : 
                threshold = float(threshold.strip("%"))/100 * suv_max
            else : 
                threshold = float(threshold)

            for point in list_points :
                if nifti_array[point[1], point[0], (slice- 1) - point[2]] <= threshold :
                    mask_4D[point[1], point[0], (slice- 1) - point[2], roi] = 0

        return mask_4D               

            
       

            

            