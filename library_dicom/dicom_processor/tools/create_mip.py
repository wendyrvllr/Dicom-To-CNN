import os
import imageio
from os.path import basename,splitext
import scipy 
import numpy as np
import matplotlib.pyplot as plt



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

def mip_projection(numpy_array, angle, path_image, borne_max=5.0):
    """create MIP Projection for a given angle

    Arguments:
        numpy_array {[array]} -- [axial view]
        angle {[int]} -- [0-360 degree]

    Keyword Arguments:
        borne_max {float} -- [description] (default: {1.0})

    Returns:
        [array] -- [numpy array 2D MIP]
    """

    numpy_array = np.transpose(np.flip(numpy_array, axis = 2), (2,1,0))

    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()

    plt.imshow(MIP, cmap = "Greys", vmax = borne_max)
    angle_filename = path_image+'\\'+'mip'+"."+str(int(angle))+".png"
    f.savefig(angle_filename, bbox_inches='tight')
    plt.close()
            
        
    return angle_filename

   

def create_mip_gif(numpy_array, path_image, borne_max = 5.0):
    duration = 0.1
    number_images = 60
    
    angle_filenames = []
    
    angles = np.linspace(0, 360, number_images)
    for angle in angles:
        path = mip_projection(numpy_array, angle, path_image, borne_max = 5.0)
        angle_filenames.append(path)
              

    create_gif(angle_filenames, duration, path_image)
       
    
    return None 