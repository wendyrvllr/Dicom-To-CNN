from library_dicom.dicom_processor.model.Fusion import Fusion 
import SimpleITK as sitk 

class FusionMask(Fusion):
    """PET and MASK = sitk image path

    Args:
        Fusion ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        self.mask_object = self.serie_ct_object
        self.mode = 'dict'
        self.pet_img, self.mask_img = self.read_nifti()

    def read_nifti(self):
        if self.mode == 'dict' : 
            pet_img = self.serie_pet_objet
            mask_img= self.mask_object

        elif self.mode == 'image' :
            pet_img, mask_img = sitk.ReadImage(self.serie_pet_objet), sitk.ReadImage(self.mask_object)
        return pet_img, mask_img

    def get_feature_pet_img(self):
        original_pixel_spacing = self.pet_img.GetSpacing()
        original_direction = self.pet_img.GetDirection()
        original_origin = self.pet_img.GetOrigin()
        original_size = self.pet_img.GetSize()
        return original_pixel_spacing, original_direction, original_origin, original_size


    def resample(self, array = False): 
        target_spacing, target_direction, target_origin, target_size = self.get_feature_pet_img()
        size = self.mask_img.GetSize()

        if len(size) == 3 : 
            transformation = sitk.ResampleImageFilter()
            transformation.SetOutputDirection(target_direction)
            transformation.SetOutputOrigin(target_origin)
            transformation.SetOutputSpacing(target_spacing)
            transformation.SetSize(target_size)
            transformation.SetDefaultPixelValue(0.0)
            transformation.SetInterpolator(sitk.sitkNearestNeighbor)
            img = transformation.Execute(self.mask_img)

        
        else : #mask 4D => mask 4D
            liste = []
            for roi in range(size[3]):
                extract = sitk.ExtractImageFilter()
                extract.setSize([size[0], size[1], size[2], 0])
                extract.setIndex([0,0,0,roi])
                extracted_img = extract.Execute(self.mask_img)
                transformation = sitk.ResampleImageFilter()
                transformation.SetOutputDirection(target_direction)
                transformation.SetOutputOrigin(target_origin)
                transformation.SetOutputSpacing(target_spacing)
                transformation.SetSize(target_size)
                transformation.SetDefaultPixelValue(0.0)
                transformation.SetInterpolator(sitk.sitkNearestNeighbor)
                new_mask_img = transformation.Execute(extracted_img)
                liste.append(new_mask_img)

            img = sitk.JoinSeries(liste)


        if array==True : 
            mask_array = sitk.GetArrayFromImage(img)
            return mask_array 

        return img

