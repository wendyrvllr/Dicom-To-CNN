import numpy as np
import matplotlib.pyplot as plt

from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
from library_dicom.dicom_processor.model.csv_reader.RoiFactory import RoiFactory
from library_dicom.dicom_processor.model.csv_reader.RoiPolygon import RoiPolygon
from library_dicom.dicom_processor.model.csv_reader.RoiElipse import RoiElipse
from library_dicom.dicom_processor.model.csv_reader.RoiNifti import RoiNifti
from library_dicom.dicom_processor.model.SeriesPT import SeriesPT


class MaskBuilder():

    def __init__(self, csv_file, matrix_size):
        self.csv_file=csv_file
        self.matrix_size=matrix_size

    def initialize_mask_matrix(self):
        self.mask_array = np.zeros( (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2], self.number_of_rois ) )

    def read_csv(self):
        """return 4D array of 3D roi array from un csv_file

        Returns:
            [array] -- [4D array of roi in csv_file]
        """
        csv_reader = CsvReader(self.csv_file)
        manual_rois = csv_reader.get_manual_rois()
        automatic_rois = csv_reader.get_nifti_rois()
        SUVlo = csv_reader.get_SUVlo()
        self.SUVlo = SUVlo 
        self.number_of_rois = len(manual_rois) + len(automatic_rois)
        self.initialize_mask_matrix() #matrice 4D
        
        for number_roi in range(4) : #pour chaque ROI du fichier #self.number_of_rois
            if len(manual_rois) == 0 : #ROI NIfti
                roi_object = csv_reader.convert_nifti_row_to_list_point(automatic_rois[number_roi])
                self.mask_array[:, :, :, number_roi] = RoiFactory(roi_object, (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2]), number_roi+1 ).read_roi().calculateMaskPoint() #return array 3D si nifti poly ou ellipse
            else : #ROI Poly ou ellipse
                roi_object = csv_reader.convert_manual_row_to_object(manual_rois[number_roi])
                self.mask_array[:, :, :, number_roi] = RoiFactory(roi_object, (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2]) , number_roi+1).read_roi().calculateMaskPoint()

             
        
        return self.mask_array
    

    #affichage 
    def show_axial_to_coronal_saggital(self, mask_array, number_roi, number_slice_axial, number_slice_coronal, number_slice_saggital):
        """to show axial, coronal and sagittal ROI

        Arguments:
            mask_array {[array]} -- [4D array of ROIs]
            number_roi {[int]} -- [number of one ROI]
            number_slice_axial {[int]} -- [number of the slice _ axial of one ROI]
            number_slice_coronal {[int]} -- [number of the slice _ coronal of one ROI]
            number_slice_saggital {[int]} -- [number of the slice _ saggital of one ROI]
        """

        
        roi_axial = mask_array[:,:,:,number_roi]
        print(roi_axial.shape)
        plt.imshow(roi_axial[:,:,number_slice_axial ])
        plt.show()
        #roi_axial = np.flip(roi_axial, axis = 2)
        roi_coronal = np.transpose(roi_axial, (2,1,0))
        print(roi_coronal.shape)
        roi_saggital  = np.transpose(roi_axial, (2,0,1))
        print(roi_saggital.shape)
        plt.imshow(roi_coronal[:,:,number_slice_coronal])
        plt.show()
        plt.imshow(roi_saggital[:,:,number_slice_saggital])
        plt.show()


    #Si z inversé => problème à gérer 

    def calcul_suv_max_mean_mask(self, series_path):
        """Calcul SUV Max et SUV Mean with SUVlo of each ROI in the CSV file 

        Arguments:
            series_path {[str]} -- [path of the PET series]

        Returns:
            [dict] -- [for each ROIs , return SUV max et SUV mean in a dict ]
        """
        series_object = SeriesPT(series_path)
        nifti_array = series_object.get_numpy_array()
        #nifti_array = np.flip(nifti_array, axis = 2)
        max_mean = {}
        #voir pour autre méthode de calcul sans trop de boucles et sans passer par tous les pixels
        for number_roi in range(4): #self.number_of_rois
            pixels_max = []
            pixels_mean = []
            results = {}
            for z in range(self.matrix_size[2]):
                for y in range(self.matrix_size[1]):
                    for x in range(self.matrix_size[0]):
                        if self.mask_array[x,y,z, number_roi] == number_roi + 1 :
                            pixels_max.append(nifti_array[x,y,z])
            
            seuil = self.SUVlo
            if "%" in seuil : 
                seuil = float(seuil.strip("%"))/100 * np.max(pixels_max)
            else : 
                seuil = float(seuil)


            for i in range(len(pixels_max)):
                if pixels_max[i] >= seuil : 
                    pixels_mean.append(pixels_max[i])
            if len(pixels_mean) == 0 :
                results['SUV_max'] = float(0)
                results['SUV_mean'] = float(0)
            else : 
                results['SUV_max'] = round(np.max(pixels_mean),2)
                results['SUV_mean'] = round(np.mean(pixels_mean),2)
            max_mean[number_roi + 1] = results
        return max_mean


    #parti check 
    def is_correct_suv(self, series_path):
        csv_reader = CsvReader(self.csv_file) #object
        data_suv = csv_reader.get_rois_suv() #liste de liste
        calculated_suv_max_mean = self.calcul_suv_max_mean_mask(series_path)#dict 
        for number_roi in range(self.number_of_rois) :
            rois_suv_object = csv_reader.convert_rois_suv_to_object(data_suv[number_roi]) #dict
            if calculated_suv_max_mean[number_roi + 1]["SUV_max"] != rois_suv_object['SUVmax'] : 
                return False
            if (calculated_suv_max_mean[number_roi + 1]["SUV_mean"] < rois_suv_object['SUVmean'] - rois_suv_object['SD'] 
                or calculated_suv_max_mean[number_roi + 1]["SUV_mean"] > rois_suv_object['SUVmean'] + rois_suv_object['SD'] ):
                return False
        return True 


    def flip_z(self, series_path): 
        if self.is_correct_suv == 'False' : 
            for number_roi in range(self.number_of_rois):
                self.mask_array[:,:,:,number_roi] = np.flip(self.mask_array[:,:,:,number_roi], axis = 2)
        return self.mask_array
            

    def is_calcul_sul_correct(self, series_path):
        series_object = SeriesPT(series_path) #objet serie
        csv_reader = CsvReader(self.csv_file) #objet csv reader
        sul_csv = csv_reader.get_SUL() #SUL du CSV 
        print(sul_csv)
        sul_calculate = round(series_object.calculateSULFactor(),5) #SUL calculé
        print(sul_calculate)
        if sul_calculate != sul_csv : 
            return False
        return True 
        


        