import os
import imageio
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from library_dicom.model.MIP_Generator import MIP_Generator

def transform_to_nan(MIP:np.ndarray):
    """[summary]

    Args:
        MIP (np.ndarray): [2D np.ndarray of MIP]
    """
    nan_MIP = np.empty(MIP.shape)
    nan_MIP[:] = np.NaN
    y,x = np.where(MIP>0)
    nan_MIP[y,x] = MIP[y,x]


def projection_two_modality(pet_array:np.ndarray, mask_array:np.ndarray, angle:int, vmin:int=0, vmax:int=7):
    mip_pet = MIP_Generator(pet_array).projection(angle)
    mip_mask = MIP_Generator(mask_array).projection(angle)
    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off() 
    plt.imshow(mip_pet, vmin=vmin, vmax=vmax, cmap='Greys', origin='lower')
    plt.imshow(mip_mask, cmap='hsv', alpha = 0.5, origin='lower')
    plt.show()
    return f

def save_projection_two_modality(figure:matplotlib.figure.Figure, filename:str, directory:str):
    figure.savefig(os.path.join(directory, filename+'.png'), bbox_inches='tight')
    plt.close()
    return os.path.join(directory, filename+'.png')

def create_gif_two_modality(pet_array:np.ndarray, mask_array:np.ndarray, filename:str, directory:str, vmin:int=0, vmax:int=7):
    duration = 0.1
    number_images = 60
    angle_filenames = []
    angles = np.linspace(0, 360, number_images)
    for angle in angles:
        f = projection_two_modality(pet_array, mask_array, angle=int(angle), vmin=vmin, vmax=vmax)
        mip_filename = str(angle)
        angle_filenames.append(save_projection_two_modality(f, mip_filename, directory))

    MIP_Generator.create_gif(angle_filenames, duration, filename, directory)
    for image in angle_filenames : 
        os.remove(image)
    return None




