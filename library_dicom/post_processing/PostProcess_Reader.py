import numpy as np
import SimpleITK as sitk 
from skimage.measure import label
#from radiomics.featureextractor import RadiomicsFeatureExtractor
import matplotlib.pyplot as plt
import scipy as sc
from sklearn import mixture

from library_dicom.post_processing.Mask3D import Mask3D
from library_dicom.post_processing.Mask4D import Mask4D


class PostProcess_Reader : 

    def __init__(self, mask_path, pet_path, type): #pt_path
        self.mask_path = mask_path
        self.pet_path = pet_path
        self.type = type

        self.pet_img = self.read_pet()
        self.pet_array = sitk.GetArrayFromImage(self.pet_img).transpose()

        self.mask_object = self.get_mask_object()
        self.binary_mask = self.get_binary_mask()
        self.binary_mask_img = self.get_binary_mask_img()

        self.labelled_mask, self.number_of_label = self.get_labelled_mask()
        self.labelled_mask_img = self.get_labelled_mask_img()

        self.new_pet_img = self.get_new_pet_array_img()
        
        #self.features = self.extract_features(self.pet_img, self.labelled_mask_img)



    def get_mask_object(self):
        if self.type == '3d' :
            return Mask3D(self.mask_path)

        elif self.type == '4d' : 
            return Mask4D(self.mask_path)

        else : 
            raise Exception ('Not a 3D or 4D mask ')
        

    def read_mask(self):
        return self.mask_object.read_mask()

    def read_pet(self):
        pt_img = sitk.ReadImage(self.pet_path)
        self.pet_origin = pt_img.GetOrigin()
        self.pet_direction = pt_img.GetDirection()
        self.pet_spacing = pt_img.GetSpacing()
        self.pet_size = pt_img.GetSize()
        return pt_img

        
    def get_binary_mask(self):
        return self.mask_object.binary_mask


    def get_binary_mask_img(self):
        new_mask_img = sitk.GetImageFromArray(self.binary_mask.transpose())
        new_mask_img.SetOrigin(self.pet_origin)
        new_mask_img.SetSpacing(self.pet_spacing)
        new_mask_img.SetDirection(self.pet_direction)
        return new_mask_img 



    def get_mask_img_spacing(self):
        return self.mask_object.get_mask_spacing()

    def get_mask_img_size(self):
        return self.mask_object.get_mask_size()
        
    def get_mask_img_origin(self):
        return self.mask_object.get_mask_origin()

    def get_mask_img_direction(self):
        return self.mask_object.get_mask_direction()
        

    def is_details_same(self):
        spacing = self.get_mask_img_spacing()
        size = self.get_mask_img_size()
        origin = self.get_mask_img_origin()
        direction = self.get_mask_img_direction()
        if (self.pet_spacing != spacing) or (self.pet_origin != origin) or (self.pet_direction != direction) or (self.pet_size != size) : 
            raise Exception ('Not the same spacing, size, origin or direction between mask and pet')

        else : return True 


    def get_labelled_mask(self):
        if len(self.binary_mask.shape) != 3 : 
            raise Exception("Not a 3D mask, need to transform into 3D binary mask")
        
        else : 
            return label(self.binary_mask, return_num = True, neighbors=4)


    def get_new_pet_array_img(self) : 
        self.pet_array[np.where(self.labelled_mask == 0)] = 0 
        pet_array = self.pet_array
        new_pet_img = sitk.GetImageFromArray(pet_array.transpose())
        new_pet_img.SetOrigin(self.pet_origin)
        new_pet_img.SetSpacing(self.pet_spacing)
        new_pet_img.SetDirection(self.pet_direction)
        return new_pet_img




    def get_labelled_mask_img(self) :
        if self.is_details_same() == True : 

            new_mask_img = sitk.GetImageFromArray(self.labelled_mask.transpose())
            new_mask_img.SetOrigin(self.pet_origin)
            new_mask_img.SetSpacing(self.pet_spacing)
            new_mask_img.SetDirection(self.pet_direction)
            return new_mask_img 

        else : raise Exception ('Cannot have labelled mask img')

    
    def extract_features(self, pet_img, mask_img):
        if pet_img.GetSize() != mask_img.GetSize() or pet_img.GetSpacing() != mask_img.GetSpacing() or pet_img.GetDirection() != mask_img.GetDirection() or pet_img.GetOrigin() != mask_img.GetOrigin() : 
            raise Exception ("Not same origin, spacing, direction or size, different img")
        else : 
            features = {}
            for label in range(1, self.number_of_label + 1 ) : 
                subdict = {}
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_img, mask_img, label = label)

                volume = results['original_shape_VoxelVolume'] * 10**(-3) #mm to ml 
                percentil_10 = results['original_firstorder_10Percentile']
                percentil_90 = results['original_firstorder_90Percentile']
                interquartile = results['original_firstorder_InterquartileRange']
                entropy = results['original_firstorder_Entropy']
                kurtosis = results['original_firstorder_Kurtosis']
                maximum = results['original_firstorder_Maximum']
                mean_abs_dev = results['original_firstorder_MeanAbsoluteDeviation']
                mean = results['original_firstorder_Mean']
                median = results['original_firstorder_Median']
                minimum = results['original_firstorder_Minimum']
                skewness = results['original_firstorder_Skewness']
                uniformity = results['original_firstorder_Uniformity']
                variance = results['original_firstorder_Variance']


                #label kurtosis/skewness
                if kurtosis == 0 : kurtosis_label = 'Mesokurtic/Normal'
                if kurtosis < 0 : kurtosis_label = 'Platykurtic'
                if kurtosis > 0 : kurtosis_label = 'Leptokurtic'

                if skewness == 0 : skewness_label = 'Symetrical/Normal'
                if skewness < 0 : skewness_label = 'Right Distribution'
                if skewness > 0 : skewness_label = 'Left Distribution'



                coordonate = np.where(self.labelled_mask == label)
                number_of_pixel = len(coordonate[0])
                subdict['volume'] = volume
                subdict['coordonate'] = coordonate
                suv_value = []
                for i in range(number_of_pixel):
                    suv_value.append(self.pet_array[coordonate[0][i], coordonate[1][i], coordonate[2][i]])
                subdict['suv_values'] = suv_value
    
                subdict['percentil_10'] = percentil_10
                subdict['percentil_90'] = percentil_90
                subdict['interquartile'] = interquartile
                subdict['entropy'] = entropy
                subdict['maximum'] = maximum
                subdict['minimum'] = minimum
                subdict['mean'] = mean
                subdict['mean_abs_dev'] = mean_abs_dev
                subdict['median'] = median
                subdict['variance'] = variance
                subdict['standart_deviation'] = np.sqrt(variance)
                subdict['uniformity'] = uniformity
                subdict['kurtosis_value'] = kurtosis
                subdict['kurtosis_label'] = kurtosis_label
                subdict['skewness_value'] = skewness
                subdict['skewness_label'] = skewness_label

                features[label] = subdict

            return features


