import matplotlib.pyplot as plt
import numpy as np 
import scipy.ndimage
import os 
from fpdf import FPDF
import imageio 

class MIP_Generator : 
    """a class to generate MIP"""

    def __init__(self, numpy_array:np.ndarray):
        """constructor

        Args:
            numpy_array (np.ndarray): [3D np.ndarray of shape (z,y,x) or 4D np.ndarray of shape (z,y,x,c)]
        """
        self.numpy_array = numpy_array

    def project(self, angle:int) -> np.ndarray:
        """function to generate 2D MIP of a 3D (or 4D) ndarray of shape (z,y,x) (or shape (z,y,x,C)) 

        Args:
            angle (int): [angle of rotation of the MIP, 0 for coronal, 90 saggital ]

        Returns:
            [np.ndarray]: [return the MIP np.ndarray]
        """
        if len(self.numpy_array.shape) == 4 : 
            array = np.amax(self.numpy_array, axis = -1)
        else : 
            array = self.numpy_array
        axis = 1 
        vol_angle = scipy.ndimage.interpolation.rotate(array , angle=angle , reshape=False, axes = (1,2))
        MIP = np.amax(vol_angle,axis=axis)
        self.MIP = MIP
        return MIP


    def save_as_png(self, filename:str, directory:str, vmin:int=0, vmax:int=7) -> str:
        """method to save matplotlib.Figure of the generated MIP as png image

        Args:
            filename (str): [name of the image]
            directory (str): [directory's path where to save the new png image]
            vmin (int, optional): [minimum value of the MIP. If mask, vmin=None]. Defaults to 0.
            vmax (int, optional): [maximum value of the MIP, If mask, vmax=None]. Defaults to 7.

        Returns : 
            (str) : [return the abs path of the saved MIP]
        """
        filename = filename+'.png'
        f = plt.figure(figsize=(10,10))
        axes = plt.gca()
        axes.set_axis_off()
        if vmin is None or vmax is None : #mask
            plt.imshow(self.MIP, cmap = 'Reds', origin='lower')
        else : #pet 
            plt.imshow(self.MIP, cmap = 'Greys', origin='lower', vmin = vmin, vmax = vmax)
        f.savefig(os.path.join(directory, filename), bbox_inches='tight')
        plt.close()
        return os.path.join(directory, filename)

    def create_mip_gif(self, filename:str, directory:str, vmin:int=0, vmax:int=7) -> None :
        """method to create mip GIF and save it as .gif

        Args:
            filename (str): [name of the gif]
            directory (str): [directory's path of the generated gif]
            vmin (int, optional): [mimimum value of the MIP]. Defaults to 0.
            vmax (int, optional): [maximum value of the MIP]. Defaults to 7.

        """
        duration = 0.1
        number_images = 60
        angle_filenames = []
        angles = np.linspace(0, 360, number_images)
        for angle in angles:
            MIP = self.project(angle)
            mip_filename=str(angle)+'.png'
            path = self.save_as_png(mip_filename, directory, vmin, vmax)
            angle_filenames.append(path)
        self.files_to_gif(angle_filenames, duration, filename, directory)
        for image in angle_filenames : 
            os.remove(image)

    @classmethod
    def files_to_gif(cls, filenames:list, duration:float, name:str, directory:str) -> None :
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
        imageio.mimwrite(output_file, images, duration=duration)

    @classmethod
    def create_pdf_mip(cls, angle_filenames:list, filename:str, directory:str)-> None : 
        """function generate pdf file of PET MIP and MASK MIP 
        
            Arguments : 
            angle_filenames ([list]) : [list of mip path and study_uid : [path_mip_pet, path_mip_mask, title], [path_mip_pet, path_mip_mask, title],... ]
            filename ([str]) : [name of the pdf file]
            directory ([str]) : [directory's path where to save the pdf file]
        """
        pdf = FPDF()
        for mip in angle_filenames : 
            pdf.add_page()
            pdf.image(mip[0], x = 0, y = 10, w = 100, h = 190)
            pdf.image(mip[1], x = 100, y = 10, w = 100, h = 190)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 0, txt= str(mip[2]), ln=2, align="C")
        pdf.output(os.path.join(directory, filename))


    

    
