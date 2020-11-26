from radiomics.featureextractor import RadiomicsFeatureExtractor 
import SimpleITK as sitk 
from itertools import combinations
import numpy as np
from library_dicom.dicom_processor.tools.threshold_mask import *





def get_center_of_mass(mask_path, thresh = False, pet_path = False):
    center = []


    if pet_path == True : 
        pet_img = sitk.ReadImage(pet_path)
        pet_array = sitk.GetArrayFromImage(pet_img).transpose()


    mask_img = sitk.ReadImage(mask_path)
    mask_array = sitk.GetArrayFromImage(mask_img).transpose()


    type_ = None 
    if len(mask_array.shape) != 3 : 
        type_ = '4D'
        origin = mask_img.GetOrigin()[0:3]
        direc = mask_img.GetDirection()
        direction = direc[0:3] + direc[4:7] + direc[8:11]
        spacing = mask_img.GetSpacing()[0:3]
        size = mask_img.GetSize()[0:3]

        pet_arr = np.random.randint(10, size=(size)).transpose()
        #pet_arr = np.ones(size).transpose()
        pet_sitk = sitk.GetImageFromArray(pet_arr)
        pet_sitk.SetOrigin(origin)
        pet_sitk.SetDirection(direction)
        pet_sitk.SetSpacing(spacing)


    else : 
        type_ = '3D'
        origin = mask_img.GetOrigin()
        direction = mask_img.GetDirection()
        spacing = mask_img.GetSpacing()
        size = mask_img.GetSize() 

        #pet_arr = np.ones(size).transpose()
        pet_arr = np.random.randint(10, size=(size)).transpose()
        pet_sitk = sitk.GetImageFromArray(pet_arr)
        pet_sitk.SetOrigin(origin)
        pet_sitk.SetDirection(direction)
        pet_sitk.SetSpacing(spacing)


    #print("pet ", pet_sitk.GetSize())
    #print("mask ", mask_img.GetSize())
    if type_ == '3D' : 
        if thresh == False : 
            number_of_roi = int(np.max(mask_array))
            for i in range(1, number_of_roi + 1) : 
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_sitk, mask_img, label = i)
                x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                center.append([x,y,z])

        elif thresh == True : 
            #ICI REVOIR 
            mask_threshold = get_threshold_matrix(mask_array, pet_array, 1, 0.41)
            mask_threshold = mask_threshold.transpose()
            new_mask = sitk.GetImageFromArray(mask_threshold)
            new_mask.SetOrigin(origin)
            new_mask.SetDirection(direction)
            new_mask.SetSpacing(spacing)
            extractor = RadiomicsFeatureExtractor()
            results = extractor.execute(pet_img, new_mask)
            x, y, z = results['diagnostics_Mask-original_CenterOfMass']
            center.append([x,y,z])


    if type_ == '4D' : 
        if thresh == False : 
            for i in range(mask_array.shape[3]):
                mask_3d = mask_array[:,:,:,i]
                mask_3d = mask_3d.transpose()
                new_mask = sitk.GetImageFromArray(mask_3d)
                new_mask.SetOrigin(origin)
                new_mask.SetDirection(direction)
                new_mask.SetSpacing(spacing)
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_sitk, new_mask)
                x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                center.append([x,y,z])
        elif thresh == True : 
            mask_4d_threshold = get_threshold_matrix_4D(mask_array, pet_array, 0.41)
            for i in range(mask_array.shape[3]):
                mask_3d = mask_4d_threshold[:,:,:,i]
                mask_3d = mask_3d.transpose()
                new_mask = sitk.GetImageFromArray(mask_3d)
                new_mask.SetOrigin(origin)
                new_mask.SetDirection(direction)
                new_mask.SetSpacing(spacing)
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_img, new_mask)
                x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                center.append([x,y,z])



    return center 

def distance(coord_A, coord_B):
    return np.sqrt((coord_A[0]-coord_B[0])**2 + (coord_A[1]-coord_B[1])**2 + (coord_A[2]-coord_B[2])**2)

def calcul_distance_max(list_center):
    comb = combinations(list_center, 2)
    comb_liste = list(comb)
    liste_distance = []
    for combinaison in comb_liste : 
        point_A = combinaison[0]
        point_B = combinaison[1]
        liste_distance.append(distance(point_A, point_B))

    #print("liste distance :", liste_distance)
    maxi = np.max(liste_distance)
    print("Max distance :", maxi)
    index = liste_distance.index(maxi)
    #print("Max distance entre les centers :", comb_liste[index])

    #print("liste des centres :", list_center)

    #numero ROI correspondante : 
    good_combi = comb_liste[index]
    roi_1 = good_combi[0]
    roi_2 = good_combi[1]
    index_roi_1 = list_center.index(roi_1)
    index_roi_2 = list_center.index(roi_2)

    print("Max de la distance entre la ROI : ", index_roi_1, "et ", index_roi_2)
    return maxi

