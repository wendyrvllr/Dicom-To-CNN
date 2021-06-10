import os 
import numpy as np
import matplotlib.pyplot as plt
from dicom_to_cnn.model.post_processing.mip.MIP_Generator import MIP_Generator

def transform_to_nan(MIP:np.ndarray) -> np.ndarray:
    """function to replace pixel with value 0 with np.NaN

    Args:
        MIP (np.ndarray): [2D np.ndarray of MIP]

    Returns:
        (np.ndarray): [2D np.ndarray NaN of MIP]
    """
    nan_MIP = np.empty(MIP.shape)
    nan_MIP[:] = np.NaN
    y,x = np.where(MIP>0)
    nan_MIP[y,x] = MIP[y,x]
    return nan_MIP 


def save_projection_two_modality(pet_array:np.ndarray, mask_array:np.ndarray, angle:int, filename:str, directory:str, vmin:int=0, vmax:int=7) -> str :
    """function to generate a MIP of PET/MASK and save it as png image

    Args:
        pet_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
        mask_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
        angle (int): [angle of the MIP rotation]
        filename (str): [filename of the png image]
        directory (str): [directory's path where to save the png image]
        vmin (int, optional): [minimum value of the PET MIP]. Defaults to 0.
        vmax (int, optional): [maximum value of the PET MIP]. Defaults to 7.

    Returns:
        [str]: [return the complete abs path to the generated PNG]
    """
    mip_pet = MIP_Generator(pet_array).projection(angle)
    mip_mask = MIP_Generator(mask_array).projection(angle)
    mip_mask = transform_to_nan(mip_mask)
    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off() 
    plt.imshow(mip_pet, vmin=vmin, vmax=vmax, cmap='Greys', origin='lower')
    plt.imshow(mip_mask, cmap='hsv', alpha = 0.5, origin='lower')
    f.savefig(os.path.join(directory, filename+'.png'), bbox_inches='tight')
    plt.close()
    return os.path.join(directory, filename+'.png')

def create_gif_two_modality(pet_array:np.ndarray, mask_array:np.ndarray, filename:str, directory:str, vmin:int=0, vmax:int=7):
    """function to generate a gif MIP of PET/MASK and save it as .gif

    Args:
        pet_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
        mask_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
        filename (str): [filename of the png image]
        directory (str): [directory's path where to save the png image]
        vmin (int, optional): [minimum value of the PET MIP]. Defaults to 0.
        vmax (int, optional): [maximum value of the PET MIP]. Defaults to 7.

    """
    duration = 0.1
    number_images = 60
    angle_filenames = []
    angles = np.linspace(0, 360, number_images)
    for angle in angles:
        mip_filename = str(angle)
        angle_filenames.append(save_projection_two_modality(pet_array, mask_array, angle, mip_filename, directory, vmin, vmax))
    MIP_Generator.create_gif(angle_filenames, duration, filename, directory)
    for image in angle_filenames : 
        os.remove(image)




