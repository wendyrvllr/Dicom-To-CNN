import numpy as np
import SimpleITK as sitk 

class Mask: 

    def __init__(self, mask_path): #pt_path
        self.mask_path = mask_path
        #self.pt_path = pt_path
        #self.pet_array = self.read_pet()
        self.mask = self.read_mask()
        self.shape_mask = self.mask.shape
        self.binary_mask = self.get_binary_mask()
        self.shape_binary_mask = self.binary_mask.shape 
    


    def read_mask(self):
        mask_img = sitk.ReadImage(self.mask_path)
        pixel_spacing = mask_img.GetSpacing()
        self.pixel_spacing = pixel_spacing #len 3 ou 4 si mask 3D ou 4D
        return sitk.GetArrayFromImage(mask_img).transpose() #[x,y,z,channel]

    #def read_pet(self):
        #pt_img = sitk.ReadImage(self.pt_path)
        #return sitk.GetArrayFromImage(pt_img).transpose()


    def get_binary_mask(self) :
        if len(self.shape_mask) != 3 :
            #si le mask est 4D 
            binary_mask = np.zeros((self.shape_mask[0], self.shape_mask[1], self.shape_mask[2]))
            sum_mask = np.ndarray.sum(self.mask, axis = -1)
            binary_mask[np.where(sum_mask != 0)] = 1
            return binary_mask.astype(np.uint8)

        else : #Si le mask est déjà en 3D (= predic = déjà binaire)
            return self.mask.astype(np.uint8)


    def get_total_lymphoma_volume(self):
        volume_pixel = self.pixel_spacing[0] * self.pixel_spacing[1] * self.pixel_spacing[2]
        volume_lymphoma = np.sum(self.binary_mask) * volume_pixel #mm

        return volume_lymphoma * 10**(-3) #ml 


    def get_connected_components(self):
        if len(self.binary_mask.shape) != 3 : 
            raise Exception("Not a 3D mask")

        else : 
            binary_img = sitk.GetImageFromArray(self.binary_mask)
            cc = sitk.ConnectedComponent(binary_img)
            stats = sitk.LabelIntensityStatisticsImageFilter()
            stats.Execute(cc, binary_img)

            number_of_labels = stats.GetLabels()
            dict = {}
            for label in number_of_labels : 
                subdict = {}
                number_of_pixel = stats.GetNumberOfPixels(label)
                subdict['number_of_pixel'] = number_of_pixel
                subdict['volume'] = self.get_volume_connected_component(number_of_pixel)
                dict[label] = subdict


        return dict 


    def get_volume_connected_component(self, number_pixel):
        volume_pixel = self.pixel_spacing[0] * self.pixel_spacing[1] * self.pixel_spacing[2]
        return volume_pixel * number_pixel * 10**(-3)
        
        






