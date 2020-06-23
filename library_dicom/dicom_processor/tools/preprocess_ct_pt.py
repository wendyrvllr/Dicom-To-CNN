import matplotlib.pyplot as plt

import tensorflow as tf
import sys

from matplotlib.backends.backend_pdf import PdfPages
from copy import copy

import numpy as np
import SimpleITK as sitk
from scipy.ndimage import zoom
import os
import random
from math import pi
from os.path import splitext,basename


def display_loading_bar(iteration,length,total_length_bar=30,add_char=None):
    """
        Display a loading bar with a iteration / length information
    """
    ac_length = round((iteration+1)/length*total_length_bar)
    loading_bar = "["+"="*ac_length+">"+"-"*(total_length_bar-ac_length)+"]"
    
    if add_char:
        sys.stdout.write("\r%s/%s %s : %s" % (str(iteration+1),str(length),loading_bar,add_char))
    else:
        sys.stdout.write("\r%s/%s %s" % (str(iteration+1),str(length),loading_bar))
        
    return None


def isometric_resample(input_img,
                       input_pixel_size,
                       output_shape=[448,176,176],
                       output_pixel_size=[4.1,4.1,4.1],
                       interpolation_order=3):
    """
        Isotropic resample:
            - zoom the input img to get the right voxel size
            - centered on the scan, crop img to the final output shape
        
        Mathematically, as we zoom exactly based on pixel size, the shape is an
        approximation, a small shift of the structures might exist
        
        Params:
            - input_img :
            - input_shape :
            - input_shape :
            - output_shape :
            - output_pixel_size :
            - interpolation_order :
    """
    input_dtype = input_img.dtype
    output_img = np.zeros(output_shape,dtype=input_dtype)

    # deform image to the output pixel size
    zoom_io = np.asarray(input_pixel_size)/np.asarray(output_pixel_size)
    input_img = zoom(input_img,
                     zoom=zoom_io,
                     order=interpolation_order,
                     mode='mirror')
    
    input_shape = input_img.shape
    
    # without deformation, incorporate zoom_input_img in output_img
    center_input  = np.asarray(input_shape)//2
    center_output = np.asarray(output_shape)//2
    
    c_min = np.minimum(center_input,center_output)
    
    cimcoi = center_input-c_min
    cipcoi = center_input+c_min
    comcii = center_output-c_min
    copcii = center_output+c_min

    output_img[comcii[0]:copcii[0],
               comcii[1]:copcii[1],
               comcii[2]:copcii[2]] = input_img[cimcoi[0]:cipcoi[0],
                                                cimcoi[1]:cipcoi[1],
                                                cimcoi[2]:cipcoi[2]]
    return output_img



def PREPROCESS(data_set_ids,path_output, output_shape=None,pixel_size=None,
                resample=True,normalize=True):
    """
            Perform preprocessing and save new datas from a dataset
            
            data_set_ids : [(PET_id_1,CT_id_1,MASK_id_1),(PET_id_2,CT_id_2,MASK_id_2)...]
    """
    n_patients = len(data_set_ids)
    
    preprocessed_data_set_ids = []

    for i,data_set_id in enumerate(data_set_ids):

            # display a loading  bar
        display_loading_bar(iteration=i,length=n_patients,add_char=basename(data_set_id[0])+'    ')

            # load data set
        PET_id, CT_id, MASK_id = data_set_id
            
        PET_img  = sitk.ReadImage(PET_id ,sitk.sitkFloat32)
        CT_img   = sitk.ReadImage(CT_id  ,sitk.sitkFloat32)
        MASK_img = sitk.ReadImage(MASK_id,sitk.sitkUInt8)

        if normalize:
            PET_img, CT_img, MASK_img = PREPROCESS_normalize(PET_img, CT_img, MASK_img)

        if resample:
            CT_img = PREPROCESS_resample_CT_to_TEP(PET_img, CT_img)
            PET_img, CT_img, MASK_img = PREPROCESS_resample_TEPCT_to_CNN(PET_img, CT_img, MASK_img, output_shape[::-1],pixel_size[::-1]) #reorder to [x,y,z]

            # save preprocess data
        new_PET_id = path_output+'/'+splitext(basename(data_set_id[0]))[0]+'.nii'
        new_CT_id   = path_output+'/'+splitext(basename(data_set_id[1]))[0]+'.nii'
        new_MASK_id   = path_output+'/'+splitext(basename(data_set_id[2]))[0]+'.nii'

        preprocessed_data_set_ids.append((new_PET_id,new_CT_id,new_MASK_id))

        PREPROCESS_save(PET_img, CT_img, MASK_img, new_filenames=preprocessed_data_set_ids[i])
        
        # clear
    #del PET_id, self.CT_id, self.MASK_id
    #del self.PET_img, self.CT_img, self.MASK_img
        
    return None


def PREPROCESS_normalize(PET_img, CT_img, MASK_img):
    """ called by PREPROCESS """
        
        # NB : possibility to add threshold values to hide artefacts
        
        # normalization TEP
    PET_img = sitk.ShiftScale(PET_img,shift=0.0, scale=1./10.)
        # normalization CT
    CT_img = sitk.ShiftScale(CT_img,shift=1000, scale=1./2000.)
        # normalization MASK
    MASK_img = sitk.Threshold(MASK_img, lower=0.0, upper=1.0, outsideValue=1.0)
        
    return PET_img, CT_img, MASK_img


def PREPROCESS_resample_CT_to_TEP(PET_img, CT_img):
    """ called by PREPROCESS """
        
    # transformation parametrisation
    transformation = sitk.ResampleImageFilter() 
    transformation.SetOutputDirection(PET_img.GetDirection())
    transformation.SetOutputOrigin(PET_img.GetOrigin())
    transformation.SetOutputSpacing(PET_img.GetSpacing())
    transformation.SetSize(PET_img.GetSize())
    transformation.SetInterpolator(sitk.sitkBSpline)

        # apply transformations on CT IMG
    CT_img = transformation.Execute(CT_img)
        
    return CT_img 


def PREPROCESS_resample_TEPCT_to_CNN(PET_img, CT_img, MASK_img, new_shape,new_spacing):
    """ called by PREPROCESS """
        
        # compute transformation parameters
    new_Origin = compute_new_Origin(PET_img, new_shape,new_spacing)
    new_Direction = PET_img.GetDirection()
        
        # transformation parametrisation
    transformation = sitk.ResampleImageFilter() 
    transformation.SetOutputDirection(new_Direction)
    transformation.SetOutputOrigin(new_Origin)
    transformation.SetOutputSpacing(new_spacing)
    transformation.SetSize(new_shape)

        # apply transformations on PET IMG
    transformation.SetInterpolator(sitk.sitkBSpline)
    PET_img = transformation.Execute(PET_img)
        # apply transformations on CT IMG
    transformation.SetInterpolator(sitk.sitkBSpline)
    CT_img = transformation.Execute(CT_img)
        # apply transformations on MASK
    transformation.SetInterpolator(sitk.sitkNearestNeighbor)
    MASK_img = transformation.Execute(MASK_img)
    return PET_img, CT_img, MASK_img 


def compute_new_Origin(PET_img, new_shape, new_spacing):
    """ called by PREPROCESS_resample """
        
    origin = np.asarray(PET_img.GetOrigin())
    shape = np.asarray(PET_img.GetSize())
    spacing = np.asarray(PET_img.GetSpacing())
    new_shape = np.asarray(new_shape)
    new_spacing = np.asarray(new_spacing)
        
    return tuple(origin+0.5*(shape*spacing-new_shape*new_spacing))

def PREPROCESS_save(PET_img, CT_img, MASK_img, new_filenames):
    """ called by PREPROCESS """

    sitk.WriteImage(PET_img,new_filenames[0])
    sitk.WriteImage(CT_img,new_filenames[1])
    sitk.WriteImage(MASK_img,new_filenames[2])
    return None