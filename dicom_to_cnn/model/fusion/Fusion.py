import numpy as np 
import SimpleITK as sitk 
import os

#target_size = (128, 128, 256)
#target_spacing = (4.0, 4.0, 4.0)
#target_direction = (1,0,0,0,1,0,0,0,1)

class Fusion: 
    """A class to resample, reshape and align PET and CT sitk Image 
    """


    def __init__(self, pet:sitk.Image, ct:sitk.Image, target_size:tuple, target_spacing:tuple, target_direction:tuple):
        """constructor

        Args:
            pet ([sitk.Image]): SeriesPT object or nifti image path or dict 
            ct([sitk.Image]): SeriesCT object or nifti image path or dict 
            target_size ([tuple]): [size (x,y,z)]
            target_spacing ([tuple]): [spacing (x,y,z)]
            target_direction ([tuple]): [direction ( x x x , y y y, z z z)]
            mode ([str]): 'serie' for serie object, 'img' if already PET and CT nifti path, 'dict' if dictionnary with img inside
        """
        self.pet_objet = pet
        self.ct_objet = ct
        self.target_size = target_size
        self.target_spacing = target_spacing
        self.target_direction = target_direction

    def get_feature_pet_img(self) -> tuple :
        """get pet spacing, size, direction, origin

        Returns:
            tuple: [return spacing, size, direction, origin value]
        """
        original_pixel_spacing = self.pet_objet.GetSpacing()
        original_direction = self.pet_objet.GetDirection()
        original_origin = self.pet_objet.GetOrigin()
        original_size = self.pet_objet.GetSize()
        return original_pixel_spacing, original_direction, original_origin, original_size

    def get_feature_ct_img(self) -> tuple :
        """get ct spacing, size, direction, origin

        Returns:
            tuple: [return spacing, size, direction, origin value]
        """
        original_pixel_spacing = self.ct_objet.GetSpacing()
        original_direction = self.ct_objet.GetDirection()
        original_origin = self.ct_objet.GetOrigin()
        original_size = self.ct_objet.GetSize()
        return original_pixel_spacing, original_direction, original_origin, original_size


    def calculate_new_origin(self, mode:str = 'head') -> tuple:
        """method to calculate new origin for both PET and CT 

        Args:
            mode (str, optional): [calculate center from head or from center]. Defaults to 'head'.

        Returns:
            [tuple]: [return new calculated center in 'head' or 'center' format]
        """
        if mode == 'head' : return self.compute_new_origin_head2hips()
        elif mode == 'center' : return self.compute_new_origin_center()

    def compute_new_origin_head2hips(self) -> tuple :
        """method to compute new_origin from head

        Returns:
            [tuple]: [return new origin]
        """
        new_size = self.target_size
        new_spacing = self.target_spacing
        pet_spacing, _, pet_origin, pet_size = self.get_feature_pet_img()
        pet_origin = np.asarray(pet_origin)
        pet_size = np.asarray(pet_size)
        pet_spacing = np.asarray(pet_spacing)
        new_origin = (pet_origin[0] + 0.5 * pet_size[0] * pet_spacing[0] - 0.5 * new_size[0] * new_spacing[0],
                      pet_origin[1] + 0.5 * pet_size[1] * pet_spacing[1] - 0.5 * new_size[1] * new_spacing[1],
                      pet_origin[2] + 1.0 * pet_size[2] * pet_spacing[2] - 1.0 * new_size[2] * new_spacing[2])
        return new_origin

    def compute_new_origin_center(self) -> tuple:
        """method to commpute new origin from center

        Returns:
            [tuple]: [return new origin]
        """
        pet_spacing, _, pet_origin, pet_size = self.get_feature_pet_img()
        pet_origin = np.asarray(pet_origin)
        pet_size = np.asarray(pet_size)
        pet_spacing = np.asarray(pet_spacing)
        new_size = np.asarray(self.target_size)
        new_spacing = np.asarray(self.target_spacing)
        return tuple(pet_origin + 0.5 * (pet_size * pet_spacing - new_size * new_spacing))

        

    def resample(self, mode:str ='head') -> sitk.Image: 
        """resample pet and ct sitk.Image with a target spacing, size, direction, and origin

        Args:
            mode (str, optional): [Choose new origin method]. Defaults to 'head'.

        Returns:
            [sitk.Image]: [return resampled pet sitk.Image and ct sitk.Image]
        """
        
        pet_img, ct_img = self.pet_objet, self.ct_objet
        
        new_origin = self.calculate_new_origin(mode=mode)
        
        #pet
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(new_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(0.0)
        transformation.SetInterpolator(sitk.sitkLinear)
        new_pet_img = transformation.Execute(pet_img) 

        #ct 
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(new_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(-1000.0)
        transformation.SetInterpolator(sitk.sitkLinear)
        new_ct_img = transformation.Execute(ct_img) 
       
        return new_pet_img, new_ct_img

    def save_nifti_fusion(self, filename:str, directory:str, mode:str ='head') -> sitk.Image:
        """save merged PT/CT nifti after resample reshape 

        Args:
            filename ([str]): [name of the merged image]
            directory ([str]): [directory's path where to save the merged image]
            mode (str, optional): [description]. Defaults to 'head'.

        Returns:
            [sitk.Image]: 4D matrix, concatenate PT/CT 
        """
        pet_img, ct_img = self.resample(mode=mode) #[c, z, y, x]
        s = []
        s.append(pet_img)
        s.append(ct_img)
        concat_img = sitk.JoinSeries(s)
        sitk.WriteImage(concat_img, os.path.join(directory,filename))
        return concat_img




