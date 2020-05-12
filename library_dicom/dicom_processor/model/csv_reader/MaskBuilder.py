from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
from library_dicom.dicom_processor.model.csv_reader.RoiFactory import RoiFactory
import numpy as np
import matplotlib.pyplot as plt

from library_dicom.dicom_processor.model.csv_reader.RoiPolygon import RoiPolygon
from library_dicom.dicom_processor.model.csv_reader.RoiElipse import RoiElipse
from library_dicom.dicom_processor.model.csv_reader.RoiNifti import RoiNifti


class MaskBuilder():

    def __init__(self, csv_file, matrix_size):
        self.csv_file=csv_file
        self.matrix_size=matrix_size

    def initialize_mask_matrix(self):
        self.mask_array = np.zeros( (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2], self.number_of_rois) )

    def read_csv(self):
        csv_reader = CsvReader(self.csv_file)
        manual_rois = csv_reader.get_manual_rois()
        automatic_rois = csv_reader.get_nifti_rois()
        self.number_of_rois = len(manual_rois) + len(automatic_rois)
        self.initialize_mask_matrix() #matrice 4D
        for number_roi in range(self.number_of_rois) : #pour chaque ROI du fichier
            if len(manual_rois) == 0 : #ROI NIfti
                roi_object = csv_reader.convert_nifti_row_to_list_point(automatic_rois[number_roi])
                self.mask_array[:, :, :, number_roi] = RoiFactory(roi_object, (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2]), self.number_of_rois ).read_roi().calculateMaskPoint() #return array 3D si nifti poly ou ellipse
            else : #ROI Poly ou ellipse
                roi_object = csv_reader.convert_manual_row_to_object(manual_rois[number_roi])
                self.mask_array[:, :, :, number_roi] = RoiFactory(roi_object, (self.matrix_size[0], self.matrix_size[1], self.matrix_size[2]) , self.number_of_rois).read_roi().calculateMaskPoint()

             
        
        return self.mask_array
    


    def show_np_array_3D(self, mask_array, slice) : 
        somme = 0 
        for i in range(self.number_of_rois) : 
            somme += mask_array[:,:,:,i]
        plt.imshow(somme[:,:,slice])
        plt.show()
    