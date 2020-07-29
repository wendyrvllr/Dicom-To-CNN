import os
import imageio
from os.path import basename,splitext
import scipy 
import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage

from fpdf import FPDF



def create_gif(filenames, duration, path_gif):
        """from a list of images, create gif 

        """

        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        
        name = splitext(basename(filenames[0][:-2]))[0]
        output_file = path_gif+'/GIF_'+name+'.gif'
        imageio.mimsave(output_file, images, duration=duration)
    
        return None

def mip_imshow(numpy_array, angle) :
    numpy_array = np.transpose(np.flip(numpy_array, axis = 2), (2,1,0)) #coronal

    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()

    plt.imshow(MIP, cmap = 'plasma')
    plt.show()


def mip_projection(numpy_array, angle, path_image, study_uid, borne_max=5.0):
    """create MIP Projection for a given angle, create .png image

    """

    numpy_array = np.transpose(np.flip(numpy_array, axis = 2), (2,1,0)) #coronal

    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()

    plt.imshow(MIP, cmap = "Greys", vmax = borne_max)
    filename = study_uid+'mip_TEP'+"."+str(int(angle))+".png"
    #angle_filename = path_image+'\\'+study_uid+'mip'+"."+str(int(angle))+".png" #rajouter le study iud du patient ou numero de serie 
    angle_filename = os.path.join(path_image, filename)
    f.savefig(angle_filename, bbox_inches='tight')
    plt.close()   
    return angle_filename



def mip_projection_4D(mask, angle, path_image, study_uid, number_roi, borne_max=5.0):
    print("taille mask : ", mask.shape)
    liste = []
    for roi in range(number_roi): 
        #print(roi)
        #pour mettre en coronal 
        liste.append(np.transpose(np.flip(mask[:,:,:,roi], axis = 2), (2,1,0)))
    
    new_mask = np.stack((liste), axis = 3)
    vol_angle = scipy.ndimage.interpolation.rotate(new_mask , angle , reshape=False, axes = (2,3))
    MIP = np.amax(vol_angle,axis=3)
    MIP2 = np.amax(MIP,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()

    plt.imshow(MIP2, cmap = "Greys", vmax = borne_max)
    filename = study_uid+'mip_MASK'+"."+str(int(angle))+".png"
    #angle_filename = path_image+'\\'+study_uid+'mip_MASK'+"."+str(int(angle))+".png" #rajouter le study iud du patient ou numero de serie 
    angle_filename = os.path.join(path_image, filename)
    f.savefig(angle_filename, bbox_inches='tight')
    plt.close()        
    return angle_filename
        

def create_pdf_mip(angle_filenames, output_path_name) : 
    """angle_filenames : [[path_mip_PET 1, path_mip_MASK 1], [path_mip_PET 2, path_mip_MASK 2],... ]

    """

    pdf = FPDF()
    for mip in angle_filenames : 
        #mip = [path_mip_PET 1, path_mip_MASK 1]
        index = angle_filenames.index(mip)
        pdf.add_page()
        pdf.image(mip[0], x = 0, y = 10, w = 100, h = 190)
        pdf.image(mip[1], x = 100, y = 10, w = 100, h = 190)
        pdf.set_font("Arial", size=12)
    
        pdf.cell(200, 0, txt= str(index), ln=2, align="C")

    pdf.output(output_path_name)

    return None 

   

def create_mip_gif(numpy_array, path_image, study_uid, borne_max = 5.0):
    """return a gif of a numpy_array MIP 

    """
    duration = 0.1
    number_images = 60
    
    angle_filenames = []
    
    angles = np.linspace(0, 360, number_images)
    for angle in angles:
        path = mip_projection(numpy_array, angle, path_image, study_uid, borne_max = 5.0)
        angle_filenames.append(path)
              

    create_gif(angle_filenames, duration, path_image)
       
    
    return None 