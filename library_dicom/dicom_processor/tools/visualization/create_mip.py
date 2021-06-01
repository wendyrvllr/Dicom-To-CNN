import os
import imageio
from os.path import basename,splitext
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage 
from PIL import Image
from fpdf import FPDF


def create_gif(filenames:list, duration:float, name:str, directory:str):
    """From a list of images, create gif

    Args:
        filenames ([list]): [list of all images' path]
        duration ([float]): [time of each image]
        name ([str]): [gif name]
        directory ([str]): [gif directory]
    """
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = directory+'/' + name +'.gif'
    imageio.mimsave(output_file, images, duration=duration)
    return None

def mip_projection(numpy_array:np.ndarray, angle:int, study_uid:str, type:str, cmap:str, vmin:int, vmax:int, directory_path:str=None):
    """function to generate MIP of a 3D (or 4D) ndarray of shape (z,y,x) (or shape (z,y,x,C)) and save it as png

    Args:
        numpy_array (np.ndarray): [3D numpy array (z,y,x) or 4D numpy array (z,y,x,C)]
        angle (int): [angle of rotation of the MIP, 0 for coronal, 90 saggital ]
        study_uid (str): [study uid of the patient]
        type (str): ['pet' or 'mask' only]
        cmap (str): [color]
        vmin (int): [minimum value of the MIP]
        vmax (int): [maximum value of the MIP]
        directory_path (str, optional): [If choose to save the MIP, set a directory's path]. Defaults to None.

    Returns:
        [str]: [return the abs path to the MIP]
    """
    if len(numpy_array.shape) == 4 : 
        numpy_array = np.sum(numpy_array, axis = -1)
    axis = 1 
    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle=angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=axis)
    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()
    if directory_path is None : 
        if type == 'mask' : 
            plt.imshow(MIP, cmap = cmap, origin='lower')
            plt.title(study_uid)
            plt.show()
            return None
        elif type == 'pet':
            plt.imshow(MIP, cmap = cmap, origin='lower', vmin = vmin, vmax = vmax)
            plt.title(study_uid)
            plt.show()
            return None 
    else : #save 
        if type == 'mask' : 
            plt.imshow(MIP, cmap = cmap, origin='lower')
            plt.title(study_uid)
            filename = study_uid+'_mip_'+type+"_"+str(int(angle))+".png"
        elif type == 'pet':
            plt.imshow(MIP, cmap = cmap, origin='lower', vmin = vmin, vmax = vmax)
            plt.title(study_uid)
            filename = study_uid+'_mip_'+type+"_"+str(int(angle))+".png"
        angle_filename = os.path.join(directory_path, filename)
        f.savefig(angle_filename, bbox_inches='tight')
        plt.close()   
        return angle_filename

def create_mip_gif(numpy_array, path_image, study_uid, type, cmap, borne_max):
    """return a gif of a numpy_array MIP 

    """
    duration = 0.1
    number_images = 60
    angle_filenames = []
    angles = np.linspace(0, 360, number_images)
    for angle in angles:
        path = mip_projection(numpy_array, angle, path_image, study_uid, type, cmap, borne_max = borne_max)
        angle_filenames.append(path)
    create_gif(angle_filenames, duration, path_image, name)
    for image in angle_filenames : 
        os.remove(image)
    return None 

def mip_pet_mask_projection(pet_array:np.ndarray, mask_array:np.ndarray, angle:int, study_uid:str, cmap_pet:str, cmap_mask:str, alpha:float, vmin:int, vmax:int, directory_path:str=None):
    """function to generate MIP of PET and MASK superposition.

    Args:
        pet_array (np.ndarray): [3D ndarray (z,y,x) or 4D ndarray (z,y,x,C)]
        mask_array (np.ndarray): [3D ndarray (z,y,x) or 4D ndarray (z,y,x,C)]
        angle (int): [angle of rotation of the MIP, 0 for coronal, 90 saggital]
        study_uid (str): [study_uid of the patient]
        cmap_pet (str): [color of PET, according to matplotlib]
        cmap_mask (str): [color of MASK, according to matplotlib ]
        alpha (float): [alpha value for transparancy of the MASK, between 0 and 1]
        vmin (int): [minimum value of PET MIP]
        vmax (int): [maximum value of PET MIP]
        directory_path (str, optional): [If choose to save the MIP, set a directory's path]. Defaults to None.

    Returns:
        [str]: [return the abs path to the MIP]
    """
    if len(pet_array.shape) == 4 : 
        pet_array = np.amax(pet_array, axis = -1)
    if len(mask_array.shape) == 4 : 
        mask_array = np.amax(mask_array, axis=-1)
    axis = 1 
    vol_angle_mask = scipy.ndimage.interpolation.rotate(mask_array , angle , reshape=False, axes = (1,2))
    MIP_mask = np.amax(vol_angle_mask,axis=axis)
    vol_angle_pet = scipy.ndimage.interpolation.rotate(pet_array , angle , reshape=False, axes = (1,2))
    MIP_pet = np.amax(vol_angle_pet,axis=axis)
    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()
    a = np.empty(MIP_mask.shape)
    a[:] = np.NaN
    for label in range(1, int(np.max(MIP_mask))+1):
        y,x = np.where(MIP_mask == label)
        a[y,x] = label
    if directory_path is None : 
        plt.imshow(MIP_pet, vmin=vmin, vmax=vmax, cmap=cmap_pet, origin='lower')
        plt.imshow(a, cmap=cmap_mask, alpha = alpha, origin='lower')
        plt.show()
        return None
    else : #save 
        plt.imshow(MIP_pet, vmin=vmin, vmax=vmax, cmap=cmap_pet, origin='lower')
        plt.imshow(a, cmap=cmap_mask, alpha = alpha, origin='lower')
        filename = study_uid + '_PET_MASK'+"_"+str(int(angle))+".png"
        angle_filename = os.path.join(directory_path, filename)
        f.savefig(angle_filename, bbox_inches='tight')
        plt.close()   
        return angle_filename


def mip_superposition_gif(pet_array:np.ndarray, mask_array:np.ndarray, study_uid:str, cmap_pet:str, cmap_mask:str, vmin:int, vmax:int ,alpha:float, directory:str, name:str):
    """Generate PET/MASK MIP superposition gif 

    Args:
        pet_array (np.ndarray): [3D ndarray (z,y,x) or 4D ndarray (z,y,x,C)]
        mask_array (np.ndarray): [3D ndarray (z,y,x) or 4D ndarray (z,y,x,C)]
        study_uid (str): [study_uid of the patient]
        cmap_pet (str): [color of PET, according to matplotlib ]
        cmap_mask (str): [color of MASK, according to matplotlib ]
        vmin (int): [minimum value of PET MIP]
        vmax (int): [maximum value of PET MIP]
        alpha (float): [alpha value for transparancy of the MASK, between 0 and 1]
        directory ([str]): [directory's path where to save the GIF]
        name ([str]): [name of the GIF]
    """
    duration = 0.1
    number_images = 60
    angles = np.linspace(0, 360, number_images)
    angles_filenames = []
    for angle in angles:
        angles_filenames.append(mip_pet_mask_projection(pet_array, mask_array, angle, study_uid, cmap_pet, cmap_mask, alpha=alpha, vmin=vmin, vmax=vmax, directory_path = directory))
    create_gif(angles_filenames, duration, name, directory)
    for image in angles_filenames : 
        os.remove(image)

def create_pdf_mip(angle_filenames:list, output_path_name:str) : 
    """function generate pdf file of PET MIP and MASK MIP 
    
        Arguments : 
        angle_filenames ([list]) : [list of mip path and study_uid : [path_mip_pet, path_mip_mask, study_uid], [path_mip_pet, path_mip_mask, study_uid],... ]
        output_path_name ([str]) : [directory+filename of the pdf file]
    """
    pdf = FPDF()
    for mip in angle_filenames : 
        pdf.add_page()
        pdf.image(mip[0], x = 0, y = 10, w = 100, h = 190)
        pdf.image(mip[1], x = 100, y = 10, w = 100, h = 190)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 0, txt= str(mip[2]), ln=2, align="C")
    pdf.output(output_path_name)
    return None 

