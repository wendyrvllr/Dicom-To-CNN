import numpy as np
import SimpleITK as sitk 
from skimage.measure import label
from radiomics.featureextractor import RadiomicsFeatureExtractor
import matplotlib.pyplot as plt
import scipy as sc
from sklearn import mixture
from pandas import DataFrame


class Mask: 

    def __init__(self, mask_path, pt_path): #pt_path
        self.mask_path = mask_path
        self.pt_path = pt_path
        self.pet_img = self.read_pet()
        self.pet_array = sitk.GetArrayFromImage(self.pet_img).transpose()
        self.mask = self.read_mask()
        self.shape_mask = self.mask.shape
        self.binary_mask = self.get_binary_mask()
        self.shape_binary_mask = self.binary_mask.shape 
        
    


    def read_mask(self):
        mask_img = sitk.ReadImage(self.mask_path)
        pixel_spacing = mask_img.GetSpacing()
        self.mask_spacing = pixel_spacing #len 3 ou 4 si mask 3D ou 4D
        #change si mask 4D ou 3D donc !!!
        self.mask_origin = mask_img.GetOrigin()
        self.mask_direction = mask_img.GetDirection()
        self.mask_size = mask_img.GetSize()
        return sitk.GetArrayFromImage(mask_img).transpose() #[x,y,z,channel]

    def read_pet(self):
        pt_img = sitk.ReadImage(self.pt_path)
        #return sitk.GetArrayFromImage(pt_img).transpose()
        self.pet_origin = pt_img.GetOrigin()
        self.pet_direction = pt_img.GetDirection()
        self.pet_spacing = pt_img.GetSpacing()
        self.pet_size = pt_img.GetSize()
        return pt_img


    def get_binary_mask(self) :
        if len(self.shape_mask) != 3 :
            #si le mask est 4D 
            binary_mask = np.zeros((self.shape_mask[0], self.shape_mask[1], self.shape_mask[2]))
            sum_mask = np.ndarray.sum(self.mask, axis = -1)
            binary_mask[np.where(sum_mask != 0)] = 1
            return binary_mask.astype(np.uint8)

        else : #Si le mask est déjà en 3D (= predic = déjà binaire)
            return self.mask.astype(np.uint8)

    def get_binary_mask_img(self, binary_mask) :
        new_mask_img = sitk.GetImageFromArray(binary_mask.transpose())
        new_mask_img.SetOrigin(self.pet_origin)
        new_mask_img.SetSpacing(self.pet_spacing)
        new_mask_img.SetDirection(self.pet_direction)
        return new_mask_img 


    def get_total_lymphoma_volume(self):
        volume_pixel = self.mask_spacing[0] * self.mask_spacing[1] * self.mask_spacing[2]
        volume_lymphoma = np.sum(self.binary_mask) * volume_pixel #mm

        return volume_lymphoma * 10**(-3) #ml 


    def get_label(self):
        if len(self.binary_mask.shape) != 3 : 
            raise Exception("Not a 3D mask, need to transform into 3D binary mask")
        
        else : 
            return label(self.binary_mask, return_num = True)


    #def get_details_label(self) :
        #dict = {}
        #labelled_mask, number_of_label = self.get_label()
        #for label in range(1, number_of_label +1) : 
            #subdict = {}
            #coordonate = np.where(labelled_mask == label)
            #number_of_pixel = len(coordonate[0])
            #subdict["coordonate"] = coordonate
            #subdict["volume"] = self.get_volume_label(number_of_pixel)
            #suv_value = []
            #for i in range(number_of_pixel):
                #suv_value.append(self.pet_array[coordonate[0][i], coordonate[1][i], coordonate[2][i]])
            #subdict['suv_values'] = suv_value
            #dict[label] = subdict
        #return dict

    def extract_features(self, pet_img, mask_img):
        if pet_img.GetSize() != mask_img.GetSize() or pet_img.GetSpacing() != mask_img.GetSpacing() or pet_img.GetDirection() != mask_img.GetDirection() or pet_img.GetOrigin() != mask_img.GetOrigin() : 
            raise Exception ("Not same origin, spacing, direction or size, different img")
        else : 
            labelled_mask, number_of_label = self.get_label()
            dict = {}
            for label in range(1, number_of_label + 1 ) : 
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



                coordonate = np.where(labelled_mask == label)
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

                dict[label] = subdict

            return dict     


    def gaussien_mixture_model(self, dict) : 
        parameters = {}
        for key in range(1, len(dict) + 1) : 
            X_train = np.asarray(dict[key]['suv_values']).reshape((-1,1))

            subdict = {}

            #find best parameters for model 
            lowest_bic = np.infty
            bic = []
            n_components_range = range(1, 8)
            cv_types = ['spherical', 'tied', 'diag', 'full']
            for cv_type in cv_types : 
                for n_components in n_components_range : 
                    gmm = mixture.GaussianMixture(n_components=n_components, covariance_type=cv_type, random_state = 0)
                    gmm.fit(X_train)

                    

                    bic.append(gmm.bic(X_train))
                    if bic[-1] < lowest_bic : 
                        lowest_bic = bic[-1]
                        best_gmm = gmm 
                        best_n_components = n_components
                        best_cv_type = cv_type
                        #mean = best_gmm.means_
                        #covariance = best_gmm.covariances_
                        #weights = best_gmm.weights_

                        labels = best_gmm.predict(X_train) #ndarray
                        


            subdict['best_n_components'] = best_n_components
            subdict['best_cv_type'] = best_cv_type
            subdict['label'] = labels

            parameters[key] = subdict

            #train model with best paramaters

            gmm_x = np.linspace(0, np.max(X_train), X_train.shape[0])
            gmm_y = np.exp(best_gmm.score_samples(gmm_x.reshape(-1,1)))


            plt.hist(dict[key]['suv_values'], bins = 'fd', normed = True, alpha = 0.6, label = 'suv_value')
            plt.xlabel('suv_value')
            plt.ylabel('frequency')
            
            plt.plot(gmm_x, gmm_y, label = 'gmm model', color = 'mediumvioletred', lw = 2)
            plt.title('roi :{}, n_components : {} , cv_type : {}'.format(key, best_n_components, best_cv_type))
            plt.legend()
            plt.show()

        return parameters


    def get_index_cluster(self, labels, n_components): #for 1 roi 
        liste = []
        for i in range(n_components) : 
            liste.append(np.where(labels == i))

        return liste 



    def get_new_clusters(self, parameters, features):
        number_of_roi = len(parameters)
        new_clusters = []
        for key in range(1, number_of_roi + 1) : 
            x,y,z = features[key]['coordonate']
            liste_new_labels = self.get_index_cluster(parameters[key]['label'], parameters[key]['best_n_components'])
            for liste in liste_new_labels : 
                subliste = []
                for index in liste[0] : 
                    subliste.append([x[index], y[index], z[index]])

                new_clusters.append(subliste)

        return new_clusters

    def get_number_total_of_roi(self, paramaters) : 
        number_of_roi = len(paramaters)
        number_total_of_roi = 0
        for key in range(1, number_of_roi + 1) : 
            new_labels = self.get_index_cluster(paramaters[key]['label'], paramaters[key]['best_n_components'])
            number_total_of_roi += len(new_labels)

        return np.arange(1, number_total_of_roi+1)


    def get_new_labelled_mask(self, paramaters, features):
        labelled_mask = np.zeros((self.shape_binary_mask[0], self.shape_binary_mask[1], self.shape_binary_mask[2]))
        liste_new_labels = self.get_number_total_of_roi(paramaters)
        coordonate_new_clusters = self.get_new_clusters(paramaters, features)
        for liste, label in zip(coordonate_new_clusters, liste_new_labels) :
            for index in liste : 
                labelled_mask[index[0], index[1], index[2]] = label

        return labelled_mask


        
    #def get_volume_label(self, number_pixel):
        #volume_pixel = self.mask_spacing[0] * self.mask_spacing[1] * self.mask_spacing[2]
        #return volume_pixel * number_pixel * 10**(-3)
