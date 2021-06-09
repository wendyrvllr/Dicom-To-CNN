import SimpleITK as sitk 
import numpy as np 

class Nifti : 
    """a class to read a nifti image, normalize et resample it 
    """

    def __init__(self, nifti_img_path:str):
        """constructor

        Args:
            nifti_img_path (str): [path of a nifti image with shape (x,y,z)]
        """
        self.nifti_img_path = nifti_img_path
        self.nifti_img = sitk.ReadImage(self.nifti_img_path) #shape (x,y,z)

    def resample_and_normalize(self, mode:str='ct') -> np.ndarray:
        """function to resample nifti_img and put it in a (1024,256,256) np.ndarray and normalize the array

        Args:
            mode (str, optional): ['ct' or other. If CT exam, keep only bones]. Defaults to 'ct'.

        Returns:
            [np.ndarray]: [return corresponding resampled and normalized np.ndarray]
        """
        spacing = self.nifti_img.GetSpacing()
        origin = self.nifti_img.GetOrigin()
        direction = self.nifti_img.GetDirection()
        size = self.nifti_img.GetSize()
        #target spacing, and size
        spacing_x = 700/256 #mm
        spacing_z = 2000/1024 #mm
        spacing_y = 700/256 #mm 

        true_x = size[0] * spacing[0] #mm
        true_y = size[1] * spacing[1] #mm 
        true_z = size[2] * spacing[2] #mm

        new_size_x = int((true_x * 256) / 700) #pixel
        new_size_y = int((true_y * 256) / 700) #pixel
        new_size_z = int((true_z * 1024) / 2000) #pixel

        #applied transformation
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(direction)
        transformation.SetOutputOrigin(origin)
        transformation.SetSize((new_size_x, new_size_y, new_size_z))
        transformation.SetOutputSpacing((spacing_x, spacing_y, spacing_z))
        transformation.SetInterpolator(sitk.sitkLinear)
        new_img = transformation.Execute(self.nifti_img)
 
        result = sitk.GetArrayFromImage(new_img) #[z,y,x]
        if mode == 'ct' : 
            result[np.where(result < 500)] = 0 #garder le squelette
            result= ((result - result.min()) * (1/(result.max() - result.min()) * 255)).astype('uint8')

        result = result[:,:,:]/255
       
        center = [512, 127, 127]
        z = int(result.shape[0]/2)
        y = int(result.shape[1]/2)
        x = int(result.shape[0]/2)

        sommet_x = center[2] - x 
        sommet_y = center[1] - y 
        sommet_z = center[0] - z
        new_array = np.zeros((1024, 256, 256))
        if result.shape[1] != 256 : 
            new_array[sommet_z:sommet_z+result.shape[0], sommet_y:sommet_y + result.shape[1], sommet_x:sommet_x + result.shape[2]] = result
        else : 
            new_array[sommet_z:sommet_z+result.shape[0],0:256, 0:256] = result
        return new_array