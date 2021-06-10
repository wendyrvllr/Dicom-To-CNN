from dicom_to_cnn.model.fusion.Fusion import Fusion 
import SimpleITK as sitk 

class FusionMask(Fusion):
    """Reshape resample aligne MASK sitk.Image to PET or CT sitk.Image

    Args:
        Fusion ([type]): [heritance from Fusion class ]
    """
    def __init__(self, pet:sitk.Image, ct:sitk.Image, target_size:tuple=None, target_spacing:tuple=None, target_direction:tuple=None):
        """constructor

        Args:
            pet (sitk.Image): [pet sitk.Image]
            ct (sitk.Image): [mask sitk.Image]
            target_size (tuple, optional): [target size]. Defaults to None.
            target_spacing (tuple, optional): [target spacing]. Defaults to None.
            target_direction (tuple, optional): [target direction]. Defaults to None.
        """
        super().__init__(pet, ct, target_size, target_spacing, target_direction)
        self.mask_objet = self.ct_objet


    def resample(self) -> sitk.Image: 
        """"resample mask sitk.Image with same spacing, size, direction, origin than PET sitk.Image

        Returns:
            [sitk.Image]: [return resampled mask img]
        """
        mask_img = self.mask_objet
        target_spacing, target_direction, target_origin, target_size = self.get_feature_pet_img()
        _, _, _, mask_size = self.get_feature_ct_img()
        
        if len(mask_size) == 3 : 
            transformation = sitk.ResampleImageFilter()
            transformation.SetOutputDirection(target_direction)
            transformation.SetOutputOrigin(target_origin)
            transformation.SetOutputSpacing(target_spacing)
            transformation.SetSize(target_size)
            transformation.SetDefaultPixelValue(0.0)
            transformation.SetInterpolator(sitk.sitkLinear)
            img = transformation.Execute(mask_img)

        
        else : 
            liste = []
            for roi in range(mask_size[3]):
                extract = sitk.ExtractImageFilter()
                extract.SetSize([mask_size[0], mask_size[1], mask_size[2], 0])
                extract.SetIndex([0,0,0,roi])
                extracted_img = extract.Execute(mask_img)
                transformation = sitk.ResampleImageFilter()
                transformation.SetOutputDirection(target_direction)
                transformation.SetOutputOrigin(target_origin)
                transformation.SetOutputSpacing(target_spacing)
                transformation.SetSize(target_size)
                transformation.SetDefaultPixelValue(0.0)
                transformation.SetInterpolator(sitk.sitkLinear)
                new_mask_img = transformation.Execute(extracted_img)
                liste.append(new_mask_img)

            img = sitk.JoinSeries(liste)

        return img

