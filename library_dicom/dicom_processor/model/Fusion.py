import numpy as np 
import SimpleITK as sitk 

#target_size = (128, 128, 256)
#target_spacing = (4.0, 4.0, 4.0)
#target_direction = (1,0,0,0,1,0,0,0,1)

class FusionPET_CT : 
    """A class to merge CT and PET after resample 
    """


    def __init__(self, serie_pet_object, serie_ct_object, target_size, target_spacing, target_direction):
        """[summary]

        Args:
            serie_pet_object ([class object]): [description]
            serie_ct_object ([class object]): [description]
            target_size ([tuple]): [size (x,y,z)]
            target_spacing ([tuple]): [spacing (x,y,z)]
            target_direction ([tuple]): [direction ( x x x , y y y, z z z)]
        """
        self.serie_pet_objet = serie_pet_object
        self.serie_ct_objet = serie_ct_object
        self.target_size = target_size
        self.target_spacing = target_spacing
        self.target_direction = target_direction

    def get_feature_pet_img(self):
        instance_array = self.serie_pet_objet.get_instances_ordered()

        original_pixel_spacing = instance_array[0].get_pixel_spacing()
        original_pixel_spacing = (float(original_pixel_spacing[0]), float(original_pixel_spacing[1]), self.serie_pet_objet.get_z_spacing())
        original_direction = instance_array[0].get_image_orientation()
        original_direction = (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]),
                                float(original_direction[3]), float(original_direction[4]), float(original_direction[5]),
                                0.0,0.0,1.0)
        original_origin =instance_array[0].get_image_position()
        original_origin = (float(original_origin[0]), float(original_origin[1]), float(original_origin[2]))
        original_size = (self.serie_pet_objet.get_size_matrix())
        return original_pixel_spacing, original_direction, original_origin, original_size


    def get_feature_ct_img(self):
        instance_array = self.serie_ct_objet.get_instances_ordered()

        original_pixel_spacing = instance_array[0].get_pixel_spacing()
        original_pixel_spacing = (float(original_pixel_spacing[0]), float(original_pixel_spacing[1]), self.serie_ct_objet.get_z_spacing())
        original_direction = instance_array[0].get_image_orientation()
        original_direction = (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]),
                                float(original_direction[3]), float(original_direction[4]), float(original_direction[5]),
                                0.0,0.0,1.0)
        original_origin =instance_array[0].get_image_position()
        original_origin = (float(original_origin[0]), float(original_origin[1]), float(original_origin[2]))
        original_size = (self.serie_ct_objet.get_size_matrix())
        return original_pixel_spacing, original_direction, original_origin, original_size



    def generate_pet_ct_img(self):
        pet_spacing, pet_direction, pet_origin, _ = self.get_feature_pet_img()
        ct_spacing, ct_direction, ct_origin, _ = self.get_feature_ct_img()

        pet_array = self.serie_pet_objet.get_numpy_array()
        ct_array = self.serie_ct_objet.get_numpy_array()
        pet_img = sitk.GetImageFromArray(np.transpose(pet_array, (2,0,1)))
        pet_img.SetSpacing(pet_spacing)
        pet_img.SetOrigin(pet_origin)
        pet_img.SetDirection(pet_direction)


        ct_img = sitk.GetImageFromArray(np.transpose(ct_array, (2,0,1)))
        ct_img.SetSpacing(ct_spacing)
        ct_img.SetOrigin(ct_origin)
        ct_img.SetDirection(ct_direction)
        
        return pet_img, ct_img



    def calculate_new_origin(self, pet_img, mode = 'head'):
        if mode == 'head' : return self.compute_new_origin_head2hips(pet_img)

        elif mode == 'center' : return self.compute_new_origin_center(pet_img)

    def compute_new_origin_head2hips(self, pet_img):
        new_size = self.target_size
        new_spacing = self.target_spacing

        pet_origin = np.asarray(pet_img.GetOrigin())
        pet_size = np.asarray(pet_img.GetSize())
        pet_spacing = np.asarray(pet_img.GetSpacing())
        new_origin = (pet_origin[0] + 0.5 * pet_size[0] * pet_spacing[0] - 0.5 * new_size[0] * new_spacing[0],
                      pet_origin[1] + 0.5 * pet_size[1] * pet_spacing[1] - 0.5 * new_size[1] * new_spacing[1],
                      pet_origin[2] + 1.0 * pet_size[2] * pet_spacing[2] - 1.0 * new_size[2] * new_spacing[2])
        return new_origin

    def compute_new_origin_center(self, pet_img):
        pet_origin = np.asarray(pet_img.GetOrigin())
        pet_size = np.asarray(pet_img.GetSize())
        pet_spacing = np.asarray(pet_img.GetSpacing())


        new_size = np.asarray(self.target_size)
        new_spacing = np.asarray(self.target_spacing)

        return tuple(pet_origin + 0.5 * (pet_size * pet_spacing - new_size * new_spacing))

        

    def resample(self, pet_img, ct_img, mode ='head'): 

        new_origin = self.calculate_new_origin(pet_img, mode=mode)

        #pet
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(new_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(0.0)
        transformation.SetInterpolator(sitk.sitkBSpline)
        new_pet_img = transformation.Execute(pet_img) 

        #ct 
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(new_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(-1000.0)
        transformation.SetInterpolator(sitk.sitkBSpline)
        new_ct_img = transformation.Execute(ct_img) 

        pet_array, ct_array = sitk.GetArrayFromImage(new_pet_img), sitk.GetArrayFromImage(new_ct_img)
        concat = np.stack([pet_array, ct_array], axis = -1)
        return concat, new_origin #concat [z, y, x, number_channel]

    def save_nifti_fusion(self, pet_img, ct_img, filename, mode ='head'):
        concat, new_origin = self.resample(pet_img, ct_img, mode=mode) #[c, z, y, x]
        s = []
        for i in range(2): 
            img = sitk.GetImageFromArray(concat[:,:,:,i])
            img.SetSpacing(self.target_spacing)
            img.SetOrigin(new_origin)
            img.SetDirection(self.target_direction)
            s.append(img)
    
        #origin, spacing, direction from pet => 4D
        concat_img = sitk.JoinSeries(s)
        sitk.WriteImage(concat_img, filename)
        return concat_img




class Fusion: 
    """A class to merge CT and PET after resample 
    """


    def __init__(self, pet, ct, target_size, target_spacing, target_direction, mode='serie'):
        """[summary]

        Args:
            pet ([class object]): SeriesPT object or nifti image or dict 
            ct([class object]): SeriesCT object or nifti image or dict 
            target_size ([tuple]): [size (x,y,z)]
            target_spacing ([tuple]): [spacing (x,y,z)]
            target_direction ([tuple]): [direction ( x x x , y y y, z z z)]
            mode ([str]): 'serie' for serie object, 'img' if already PET and CT nifti 
        """
        self.serie_pet_objet = pet
        self.serie_ct_objet = ct
        self.target_size = target_size
        self.target_spacing = target_spacing
        self.target_direction = target_direction
        self.mode = mode

    def get_feature_pet_img(self):
        if self.mode == 'serie' : 
            instance_array = self.serie_pet_objet.get_instances_ordered()

            original_pixel_spacing = instance_array[0].get_pixel_spacing()
            original_pixel_spacing = (float(original_pixel_spacing[0]), float(original_pixel_spacing[1]), self.serie_pet_objet.get_z_spacing())
            original_direction = instance_array[0].get_image_orientation()
            original_direction = (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]),
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]),
                                    0.0,0.0,1.0)
            original_origin =instance_array[0].get_image_position()
            original_origin = (float(original_origin[0]), float(original_origin[1]), float(original_origin[2]))
            original_size = (self.serie_pet_objet.get_size_matrix())
            return original_pixel_spacing, original_direction, original_origin, original_size

        else : 
            pet_img = sitk.ReadImage(self.serie_pet_objet)
            original_pixel_spacing = pet_img.GetSpacing()
            original_direction = pet_img.GetDirection()
            original_origin = pet_img.GetOrigin()
            original_size = pet_img.GetSize()
            return original_pixel_spacing, original_direction, original_origin, original_size

    def get_feature_ct_img(self):
        instance_array = self.serie_ct_objet.get_instances_ordered()

        original_pixel_spacing = instance_array[0].get_pixel_spacing()
        original_pixel_spacing = (float(original_pixel_spacing[0]), float(original_pixel_spacing[1]), self.serie_ct_objet.get_z_spacing())
        original_direction = instance_array[0].get_image_orientation()
        original_direction = (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]),
                                float(original_direction[3]), float(original_direction[4]), float(original_direction[5]),
                                0.0,0.0,1.0)
        original_origin =instance_array[0].get_image_position()
        original_origin = (float(original_origin[0]), float(original_origin[1]), float(original_origin[2]))
        original_size = (self.serie_ct_objet.get_size_matrix())
        return original_pixel_spacing, original_direction, original_origin, original_size



    def generate_pet_ct_img(self):
        if self.mode == 'serie' : 
            pet_spacing, pet_direction, pet_origin, _ = self.get_feature_pet_img()
            ct_spacing, ct_direction, ct_origin, _ = self.get_feature_ct_img()

            pet_array = self.serie_pet_objet.get_numpy_array()
            ct_array = self.serie_ct_objet.get_numpy_array()
            pet_img = sitk.GetImageFromArray(np.transpose(pet_array, (2,0,1)))
            pet_img.SetSpacing(pet_spacing)
            pet_img.SetOrigin(pet_origin)
            pet_img.SetDirection(pet_direction)


            ct_img = sitk.GetImageFromArray(np.transpose(ct_array, (2,0,1)))
            ct_img.SetSpacing(ct_spacing)
            ct_img.SetOrigin(ct_origin)
            ct_img.SetDirection(ct_direction)
            
            return pet_img, ct_img

        else : 
            return sitk.ReadImage(self.serie_pet_objet), sitk.ReadImage(self.serie_ct_objet)



    def calculate_new_origin(self, pet_img, mode = 'head'):
        if mode == 'head' : return self.compute_new_origin_head2hips(pet_img)

        elif mode == 'center' : return self.compute_new_origin_center(pet_img)

    def compute_new_origin_head2hips(self, pet_img):
        new_size = self.target_size
        new_spacing = self.target_spacing

        pet_origin = np.asarray(pet_img.GetOrigin())
        pet_size = np.asarray(pet_img.GetSize())
        pet_spacing = np.asarray(pet_img.GetSpacing())
        new_origin = (pet_origin[0] + 0.5 * pet_size[0] * pet_spacing[0] - 0.5 * new_size[0] * new_spacing[0],
                      pet_origin[1] + 0.5 * pet_size[1] * pet_spacing[1] - 0.5 * new_size[1] * new_spacing[1],
                      pet_origin[2] + 1.0 * pet_size[2] * pet_spacing[2] - 1.0 * new_size[2] * new_spacing[2])
        return new_origin

    def compute_new_origin_center(self, pet_img):
        pet_origin = np.asarray(pet_img.GetOrigin())
        pet_size = np.asarray(pet_img.GetSize())
        pet_spacing = np.asarray(pet_img.GetSpacing())


        new_size = np.asarray(self.target_size)
        new_spacing = np.asarray(self.target_spacing)

        return tuple(pet_origin + 0.5 * (pet_size * pet_spacing - new_size * new_spacing))

        

    def resample(self, mode ='head'): 
        pet_img, ct_img = self.generate_pet_ct_img()
        new_origin = self.calculate_new_origin(pet_img, mode=mode)
        
        #pet
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(new_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(0.0)
        transformation.SetInterpolator(sitk.sitkBSpline)
        new_pet_img = transformation.Execute(pet_img) 

        #ct 
        transformation = sitk.ResampleImageFilter()
        transformation.SetOutputDirection(self.target_direction)
        transformation.SetOutputOrigin(new_origin)
        transformation.SetOutputSpacing(self.target_spacing)
        transformation.SetSize(self.target_size)
        transformation.SetDefaultPixelValue(-1000.0)
        transformation.SetInterpolator(sitk.sitkBSpline)
        new_ct_img = transformation.Execute(ct_img) 


        if mode == 'dict' : 
            return new_pet_img, new_ct_img


        pet_array, ct_array = sitk.GetArrayFromImage(new_pet_img), sitk.GetArrayFromImage(new_ct_img)
        concat = np.stack([pet_array, ct_array], axis = -1)
        return concat, new_origin #concat [z, y, x, number_channel]

    def save_nifti_fusion(self, pet_img, ct_img, filename, mode ='head'):
        """save merged PT/CT nifti after resample reshape 

        Args:
            pet_img ([type]): [description]
            ct_img ([type]): [description]
            filename ([type]): [description]
            mode (str, optional): [description]. Defaults to 'head'.

        Returns:
            [type]: 4D matrix, concatenate PT/CT 
        """
        concat, new_origin = self.resample(pet_img, ct_img, mode=mode) #[c, z, y, x]
        s = []
        for i in range(2): 
            img = sitk.GetImageFromArray(concat[:,:,:,i])
            img.SetSpacing(self.target_spacing)
            img.SetOrigin(new_origin)
            img.SetDirection(self.target_direction)
            s.append(img)
    
        #origin, spacing, direction from pet => 4D
        concat_img = sitk.JoinSeries(s)
        sitk.WriteImage(concat_img, filename)
        return concat_img