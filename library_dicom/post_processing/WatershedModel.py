import numpy as np
import SimpleITK as sitk 
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage import segmentation
from library_dicom.post_processing.PostProcess_Reader import PostProcess_Reader

class WatershedModel(PostProcess_Reader):

    def __init__(self, mask_path, pet_path, type):
        super().__init__(mask_path, pet_path, type)
    

    def get_labels_for_model(self, labelled_threshold_img):
        label = []
        results = self.label_stat_results(labelled_threshold_img)
        for key in range(1, len(results)) :
            if results[key]['volume'] > float(40) :
                label.append(key)

        return label

    def get_label_threshold_matrix(self, label, labelled_threshold_mask):
        x,y,z = self.size_matrix
        new_matrix = np.zeros((x,y,z))
        new_matrix[np.where(labelled_threshold_mask == label)] = self.pet_array[np.where(labelled_threshold_mask== label)]
        return new_matrix

    def get_distance_map(self, threshold_matrix):
        return ndimage.distance_transform_edt(threshold_matrix)

    def get_local_peak(self, distance_map):
        return peak_local_max(distance_map, indices = True, min_distance=41)

    def define_marker_array(self, localMax):
        marker_array = np.zeros(self.size_matrix)
        for marker in range(len(localMax)) : 
            marker_array[localMax[marker][0], localMax[marker][1], localMax[marker][2]] = marker + 1

        return marker_array.astype(np.uint8)

    def get_number_of_localMax(self, localMax):
        return len(localMax)

    def watershed_segmentation(self, distance_map, marker_array, mask) : 
        labels = segmentation.watershed(distance_map, marker_array, mask = mask)
        return labels.astype(np.uint8)


    def watershed_model(self, threshold) : 
        binary_threshold_mask_img = self.get_binary_threshold_mask_img(threshold)

        labelled_threshold_img = self.get_labelled_threshold_mask_img(binary_threshold_mask_img)
        labelled_threshold_array = self.get_labelled_threshold_mask_array(labelled_threshold_img)


        stats_results = self.label_stat_results(labelled_threshold_img)
        label_coordonate = self.label_coordonate(labelled_threshold_array, stats_results)
        labels_for_model = self.get_labels_for_model(labelled_threshold_img)
        for label in labels_for_model : 
            new_mask = self.get_label_threshold_matrix(label, labelled_threshold_array)
            distance_map = self.get_distance_map(new_mask)
            localMax = self.get_local_peak(distance_map)
            number_localMax = self.get_number_of_localMax(localMax)
            marker_array = self.define_marker_array(localMax)
            new_distance_map = -1 * distance_map
            new_label_mask = self.watershed_segmentation(new_distance_map, marker_array, new_mask)

            new_coordonate = []
            for new_label in range(1, number_localMax + 1):
                new_coordonate.append(np.where(new_label_mask == new_label))

            label_coordonate[label] = new_coordonate

        #number_total_of_label = 0
        #for key in range(len(label_coordonate)) :
            #number_total_of_label += len(label_coordonate[key])

        #liste_label = np.arange(1, number_total_of_label + 1, 1)

        liste_coordonate = self.extract_coordonate(label_coordonate)
        number_total_of_label = len(liste_coordonate)
        print(number_total_of_label)
        liste_label = liste_label = np.arange(1, number_total_of_label + 1, 1)

        return self.watershed_matrix(liste_coordonate, liste_label), label_coordonate


    def extract_coordonate(self, results):
        liste = []
        for key in range(1, len(results) + 1) : 
            for i in range(len(results[key])) : 
                liste.append(results[key][i])

        return liste 

    def watershed_matrix(self, liste_coordonate, liste_label) :
        ws_matrix = np.zeros(self.size_matrix)
        for coordonate, label in zip(liste_coordonate, liste_label) :
            ws_matrix[coordonate] = label

        return ws_matrix.astype(np.uint8)

