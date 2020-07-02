import numpy as np
import matplotlib.pyplot as plt

from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
from library_dicom.dicom_processor.model.csv_reader.RoiFactory import RoiFactory
from library_dicom.dicom_processor.model.csv_reader.RoiPolygon import RoiPolygon
from library_dicom.dicom_processor.model.csv_reader.RoiElipse import RoiElipse
from library_dicom.dicom_processor.model.csv_reader.RoiNifti import RoiNifti
from library_dicom.dicom_processor.model.SeriesPT import SeriesPT


class MaskBuilder(CsvReader):
    """Class to build mask from a csv file 

    Arguments:
        CsvReader {[class]} -- [description]
    """

    def __init__(self, csv_path, matrix_size):
        super().__init__(csv_path)
        self.matrix_size=matrix_size
        self.number_of_rois = len(self.details_rois) - 2 #moins ligne SUL + ligne SUClo
        self.mask_array = self.build_mask()

        


    def initialize_mask_matrix(self):
        """build empty 4D numpy array 
        """
        self.mask_array = np.zeros( (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2], self.number_of_rois )).astype(np.uint8)


    def build_mask(self):
        """build 3D numpy array mask with ROI coordonates from a CSV, put in a 4D matrix

        """
        self.initialize_mask_matrix()
        for number_roi in range(1 ,  self.number_of_rois + 1):
            #print(number_roi)
            roi_object = RoiFactory(self.details_rois[number_roi], (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2]) , number_roi).read_roi() #.list_points
            list_points = roi_object.list_points
            np_array_3D = roi_object.get_mask(list_points, number_roi) #3D_array

            self.mask_array[:,:,:,number_roi - 1] = np_array_3D

            if roi_object.type_number == 2 or roi_object.type_number == 12 :  
                #print("coronal")
                new_list_points = self.coronal_list_points_to_axial(list_points)
                self.details_rois[number_roi]['list_points'] = new_list_points
            
            elif roi_object.type_number == 3 or roi_object.type_number == 13 :
                #print("saggital")
                new_list_points = self.saggital_list_points_to_axial(list_points)
                self.details_rois[number_roi]['list_points'] = new_list_points

            #axial
            else : self.details_rois[number_roi]['list_points'] = list_points
            
        
        return self.mask_array.astype(np.uint8) #liste


    def coronal_list_points_to_axial(self, list_points):
        """ Change the list_points in coronal to axial 
        coronal           axial 
          x                 z
          y                 y
          z                 x
        """
 
        new_list_points = []
        for point in list_points : 
            new_point = []
            new_point.append(point[0])
            new_point.append(point[2])
            new_point.append(point[1]) 
            new_list_points.append(new_point)

        return new_list_points



    #A REPRENDRE
    def saggital_list_points_to_axial(self, list_points) : 
        """ Change the list_points in saggital to coronal 
        saggital           axial 
          x                 x
          y                 z
          z                 y
        """
        new_list_points = []
        for point in list_points : 
            new_point = []
            new_point.append(point[1])
            new_point.append(point[2])
            new_point.append(point[0])
            new_list_points.append(new_point)

        return new_list_points



    def calcul_suv(self, nifti_array, flip = False):
        """calcul SUV Mean, SUV Max and SD from the 3D np array of a mask and put results in a dict
        """
        slice = nifti_array.shape[2]
        max_mean = {}
        for number_roi in range(1 , self.number_of_rois + 1):
            #print("ROI :", number_roi)
            list_points = self.details_rois[number_roi]['list_points'] #[[x,y,z], [x,y,z],...]
            list_pixels = []
            list_pixels_seuil = []
            results = {}
            for point in list_points :
                if (flip == True) : 
                    list_pixels.append(nifti_array[point[1], point[0], (slice- 1) - point[2]]) 
                #transpose x et y dans les matrices 3D 
                else : 
                    list_pixels.append(nifti_array[point[1], point[0], point[2]])



            if list_pixels == [] : #si pas de ROI dessiné
                results['SUV_max'] = float(0)
                results['SUV_mean'] = float(0)
                results['SD'] = float(0)


            else : 
                seuil = self.details_rois['SUVlo']


                if "%" in seuil : 
                    seuil = float(seuil.strip("%"))/100 * np.max(list_pixels)
                else : 
                    seuil = float(seuil)

            
                for i in range(len(list_pixels)):
                    if list_pixels[i] >= seuil : 
                        list_pixels_seuil.append(list_pixels[i])

                if len(list_pixels_seuil) == 0 :
                    results['SUV_max'] = float(0)
                    results['SUV_mean'] = float(0)
                    results['SD'] = float(0)
                else : 
                    #results['pixel_number'] = len(list_pixels_seuil)
                    results['SUV_max'] = round(np.max(list_pixels_seuil), 2)
                    results['SUV_mean'] = round(np.mean(list_pixels_seuil), 2)
                    results['SD'] = round(np.std(list_pixels_seuil), 2)
            
            max_mean[number_roi] = results

        return max_mean


    #parti check 
    def is_correct_suv(self, nifti_array, flip = False):
        """check if calculated SUV Mean SUV Max and SD is correct 

        """

        calculated_suv_max_mean = self.calcul_suv(nifti_array, flip) #dict 
        for number_roi in range(1, self.number_of_rois +1) :

            if (calculated_suv_max_mean[number_roi]['SUV_max'] < float(self.details_rois[number_roi]['suv_max']) - float(0.1) or 
                calculated_suv_max_mean[number_roi]['SUV_max'] > float(self.details_rois[number_roi]['suv_max']) + float(0.1)  ):
                return False


            if (calculated_suv_max_mean[number_roi]['SUV_mean']  < float(self.details_rois[number_roi]['suv_mean']) - float(0.1) or 
                calculated_suv_max_mean[number_roi]['SUV_mean']  > float(self.details_rois[number_roi]['suv_mean']) + float(0.1) ) : 
                return False

            if (calculated_suv_max_mean[number_roi]['SD'] < float(self.details_rois[number_roi]['sd']) - float(0.1) or 
                calculated_suv_max_mean[number_roi]['SD'] > float(self.details_rois[number_roi]['sd']) + float(0.1) ) :
                return False

        return True 





    def ecart_suv_max(self, nifti_array, flip = False):
        
        liste = []
        calculated_suv_max_mean = self.calcul_suv(nifti_array, flip) #dict 
        for number_roi in range(1, self.number_of_rois +1) :

            #print(number_roi)

            if (calculated_suv_max_mean[number_roi]['SUV_max'] < float(self.details_rois[number_roi]['suv_max']) - float(0.1) or 
                calculated_suv_max_mean[number_roi]['SUV_max'] > float(self.details_rois[number_roi]['suv_max']) + float(0.1)  ):
                type_roi = self.details_rois[number_roi]['type_number']
                liste.append(number_roi)
                if type_roi == 1 or type_roi == 2 or type_roi == 3 : 
                    liste.append("POLYGON")

                if type_roi == 11 or type_roi == 12 or type_roi == 13 : 
                    liste.append("ELLIPSE")

                liste.append(float(abs(calculated_suv_max_mean[number_roi]['SUV_max'] - float(self.details_rois[number_roi]['suv_max']))))
                

        return liste 

    def ecart_suv_mean(self, nifti_array, flip = False ) : 
        liste = []
        calculated_suv_max_mean = self.calcul_suv(nifti_array, flip) #dict 
        for number_roi in range(1, self.number_of_rois +1) :

            #print(number_roi)

            if (calculated_suv_max_mean[number_roi]['SUV_mean'] < float(self.details_rois[number_roi]['suv_mean']) - float(0.1) or 
                calculated_suv_max_mean[number_roi]['SUV_mean'] > float(self.details_rois[number_roi]['suv_mean']) + float(0.1)):
                type_roi = self.details_rois[number_roi]['type_number']
                liste.append(number_roi)
                if type_roi == 1 or type_roi == 2 or type_roi == 3 : 
                    liste.append("POLYGON")

                if type_roi == 11 or type_roi == 12 or type_roi == 13 : 
                    liste.append("ELLIPSE")

                liste.append(float(abs(calculated_suv_max_mean[number_roi]['SUV_mean'] - float(self.details_rois[number_roi]['suv_mean']))))
                

        return liste 


    def ecart_SD(self, nifti_array, flip = False) :
        liste = []
        calculated_suv_max_mean = self.calcul_suv(nifti_array, flip) #dict 
        for number_roi in range(1, self.number_of_rois +1) :

            #print(number_roi)

            if (calculated_suv_max_mean[number_roi]['SD'] < float(self.details_rois[number_roi]['sd']) - float(0.1) or 
                calculated_suv_max_mean[number_roi]['SD'] > float(self.details_rois[number_roi]['sd']) + float(0.1)):
                type_roi = self.details_rois[number_roi]['type_number']
                liste.append(number_roi)
                if type_roi == 1 or type_roi == 2 or type_roi == 3 : 
                    liste.append("POLYGON")

                if type_roi == 11 or type_roi == 12 or type_roi == 13 : 
                    liste.append("ELLIPSE")

                liste.append(float(abs(calculated_suv_max_mean[number_roi]['SD'] - float(self.details_rois[number_roi]['sd']))))
                

        return liste 



    def flip_z(self, mask_4D): 
        """flip z axis in the mask matrix if calculated SUV Mean SUV MAX and SD is False 

        """
        slice = mask_4D.shape[2]
    
        liste = []
        for number_roi in range(self.number_of_rois):
            
            new_list_point = []

            liste.append(np.flip(mask_4D[:,:,:,number_roi], axis = 2))
            
            if self.details_rois[number_roi + 1]['list_points'] != [] :
                for point in self.details_rois[number_roi + 1]['list_points'] : 
                    new_z = slice - 1 - point[2]
                    point[2] = new_z

                    new_list_point.append(point)
        
            self.details_rois[number_roi + 1]['list_points'] = new_list_point
        #print(len(liste))
        #print("après flip :", self.details_rois[1]['list_points'][0])
        self.mask_array = np.stack((liste), axis = 3)
        return self.mask_array


            

    def is_calcul_sul_correct(self, series_path):
        """check if the SUL in the CSV file and the calculated SUL is the same 

        """
        series_object = SeriesPT(series_path) 
        sul_calculate = round(series_object.calculateSULFactor(),5) 
        sul_csv = self.details_rois['SUL']
        if sul_calculate != sul_csv : 
            return False
        return True 
        

        