import json
import os
from library_dicom.dicom_processor.model.Series import Series 
from library_dicom.dicom_processor.model.SeriesPT import SeriesPT
from library_dicom.dicom_processor.model.SeriesCT import SeriesCT
from library_dicom.dicom_processor.model.csv_reader.MaskBuilder import MaskBuilder
from library_dicom.dicom_processor.model.FusionPET_CT import FusionPET_CT

from library_dicom.dicom_processor.tools.folders import *

from library_dicom.dicom_processor.tools.create_mip import *
from library_dicom.dicom_processor.tools.threshold_mask import *

import numpy as np
import SimpleITK as sitk

import csv



json_path = '/media/deeplearning/Elements/REMARC_Validated_DICOMS/REMARC_dataset.json'
dataset = []
with open(json_path) as json_file : 
    reader = json.load(json_file)
    for info in reader :
        dataset.append(info)


number_of_study = len(dataset)
print("number of study : ", number_of_study)



csv_path = '/media/deeplearning/Elements/REMARC_csv'
liste_csv_file = os.listdir(csv_path)
liste_csv = []
for csv_file in liste_csv_file : 
    liste_csv.append(os.path.join(csv_path, csv_file))



for data in dataset : 
    for csv_f in liste_csv : 
        if data[-1] in csv_f : 
            data.append(csv_f)



check_csv = []
for data in dataset : 
    if len(data) != 8 : 
        check_csv.append(data)

print(len(check_csv))
write_json_file('/media/deeplearning/Elements/REMARC_Validated_DICOMS', 'check_csv', check_csv)

for r in check_csv : 
    dataset.remove(r)



for data in dataset : 
    new_1 = data[0].replace('/media/oncopole/DD 2To', '/media/deeplearning/Elements')
    new_2 = data[2].replace('/media/oncopole/DD 2To', '/media/deeplearning/Elements')
    data[0] = new_1
    data[2] = new_2

print('Nombre de study : ', len(dataset))

write_json_file('/media/deeplearning/Elements/REMARC_Validated_DICOMS', 'validated_dataset', dataset)


target_size = (128, 128, 256)
target_spacing = (4.0, 4.0, 4.0)
target_direction = (1,0,0,0,1,0,0,0,1)

nifti_directory = '/media/deeplearning/Elements/REMARC_NIFTI'
mip_directory = '/media/deeplearning/Elements/REMARC_MIP'

#save serie_path with false mask 
serie_false_mask = []
#save result about serie with false mask 
results_false_mask = []
#save path of MIP to generate PDF 
path_mip = []

#save error serie 
error_dataset = []

for serie in [dataset[91]]: 
    try : 
        print(dataset.index(serie))
        subliste = []
        if serie[1] == 'PT' : 
            
            serie_pt_objet = SeriesPT(serie[0])
            serie_pt_objet.get_instances_ordered()
            nifti_array = serie_pt_objet.get_numpy_array()
            study_uid = serie_pt_objet.get_series_details()['study']['StudyInstanceUID']
            size_matrix = serie_pt_objet.get_size_matrix()
            mask_objet = MaskBuilder(serie[-1], size_matrix)
            mask_4D = mask_objet.mask_array

            number_roi = mask_4D.shape[3]
            threshold = mask_objet.details_rois['SUVlo']

            if mask_objet.is_correct_suv(nifti_array) == True : 

                print("MASK CORRECT")
                #generation nifti PT
                filename_pt = study_uid+'_'+'nifti_'+'PT'+'.nii'
                serie_pt_objet.export_nifti(os.path.join(nifti_directory, filename_pt))
                print("EXPORT NIFTI PT")

                #generation nifti CT
                serie_ct_objet = SeriesCT(serie[2])
                serie_ct_objet.get_instances_ordered()
                serie_ct_objet.get_numpy_array()
                filename_ct = study_uid+'_'+'nifti_'+'CT'+'.nii'
                serie_ct_objet.export_nifti(os.path.join(nifti_directory, filename_ct))
                print("EXPORT NIFTI CT")

                #generation nifti mask
                filename_mask = study_uid+'_'+'nifti_'+'mask'+'.nii'
                serie_pt_objet.export_nifti(os.path.join(nifti_directory, filename_mask), mask_4D)
                print("EXPORT NIFTI MASK")

                #generation merged PT/CT
                filename_merged = study_uid+'_'+'nifti_'+'merged'+'.nii'
                fusion_objet = FusionPET_CT(serie_pt_objet, serie_ct_objet, target_size, target_spacing, target_direction)
                pet_img, ct_img = fusion_objet.generate_pet_ct_img()
                merged_img = fusion_objet.save_nifti_fusion(pet_img, ct_img, os.path.join(nifti_directory, filename_merged), mode ='head')
                print("EXPORT NIFTI MERGED")




            else : 
                results = []
                print("FALSE MASK")
                serie_false_mask.append(serie)

                print(mask_objet.calcul_suv(nifti_array))
                results.append(mask_objet.calcul_suv(nifti_array))

                print(mask_objet.ecart_suv_max(nifti_array))
                results.append(mask_objet.ecart_suv_max(nifti_array))

                print(mask_objet.ecart_suv_mean(nifti_array))
                results.append(mask_objet.ecart_suv_mean(nifti_array))

                print(mask_objet.ecart_SD(nifti_array))
                results.append(mask_objet.ecart_SD(nifti_array))

                results_false_mask.append(results)

                #threshold mask 41% 
                mask_4D = threshold_matrix(mask_4D, nifti_array, 0.41)

                #create mip for false mask and check 
                #pet
                angle_filename = mip_projection(nifti_array, 0, mip_directory, study_uid, 'pet', cmap='Greys', vmin=0, vmax=7) 
                subliste.append(angle_filename)
                print('MIP PET')
                #mask
                angle_filename_mask = mip_projection_4D(mask_4D, 0, mip_directory, study_uid, number_roi, cmap='Greys')
                subliste.append(angle_filename_mask)
                print('MIP MASK')
                path_mip.append(subliste)


        else : 
            serie_pt_objet = SeriesPT(serie[2])
            serie_pt_objet.get_instances_ordered()
            nifti_array = serie_pt_objet.get_numpy_array()
            study_uid = serie_pt_objet.get_series_details()['study']['StudyInstanceUID']
            size_matrix = serie_pt_objet.get_size_matrix()
            mask_objet = MaskBuilder(serie[-1], size_matrix)
            mask_4D = mask_objet.mask_array

            number_roi = mask_4D.shape[3]
            threshold = mask_objet.details_rois['SUVlo']

            if mask_objet.is_correct_suv(nifti_array) == True :  
                print("MASK CORRECT")
                #generation nifti PT
                filename_pt = study_uid+'_'+'nifti_'+'PT'+'.nii'
                serie_pt_objet.export_nifti(os.path.join(nifti_directory, filename_pt))
                print("EXPORT NIFTI PT")

                #generation nifti CT
                serie_ct_objet = SeriesCT(serie[0])
                serie_ct_objet.get_instances_ordered()
                serie_ct_objet.get_numpy_array()
                filename_ct = study_uid+'_'+'nifti_'+'CT'+'.nii'
                serie_ct_objet.export_nifti(os.path.join(nifti_directory, filename_ct))
                print("EXPORT NIFTI CT")

                #generation nifti mask
                filename_mask = study_uid+'_'+'nifti_'+'mask'+'.nii'
                serie_pt_objet.export_nifti(os.path.join(nifti_directory, filename_mask), mask_4D)
                print("EXPORT NIFTI MASK")

                #generation merged PT/CT
                filename_merged = study_uid+'_'+'nifti_'+'merged'+'.nii'
                fusion_objet = FusionPET_CT(serie_pt_objet, serie_ct_objet, target_size, target_spacing, target_direction)
                pet_img, ct_img = fusion_objet.generate_pet_ct_img()
                merged_img = fusion_objet.save_nifti_fusion(pet_img, ct_img, os.path.join(nifti_directory, filename_merged), mode ='head')
                print("EXPORT NIFTI MERGED")




            else : 
                results = []
                print("FALSE MASK")
                serie_false_mask.append(serie)

                print(mask_objet.calcul_suv(nifti_array))
                results.append(mask_objet.calcul_suv(nifti_array))

                print(mask_objet.ecart_suv_max(nifti_array))
                results.append(mask_objet.ecart_suv_max(nifti_array))

                print(mask_objet.ecart_suv_mean(nifti_array))
                results.append(mask_objet.ecart_suv_mean(nifti_array))

                print(mask_objet.ecart_SD(nifti_array))
                results.append(mask_objet.ecart_SD(nifti_array))

                results_false_mask.append(results)

                #threshold mask 41% 
                mask_4D = threshold_matrix(mask_4D, nifti_array, 0.41)

                #create mip for false mask and check 
                #pet
                angle_filename = mip_projection(nifti_array, 0, mip_directory, study_uid, 'pet', cmap='Greys', vmin=0, vmax=7) 
                subliste.append(angle_filename)
                print("MIP PET")
                #mask
                angle_filename_mask = mip_projection_4D(mask_4D, 0, mip_directory, study_uid, number_roi, cmap='Greys')
                subliste.append(angle_filename_mask)
                print('MIP MASK ')
                path_mip.append(subliste)
               

    except Exception as err : 
        print(serie)
        print(err)
        error_dataset.append(serie)