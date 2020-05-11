from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
import numpy as np

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
        self.initialize_mask_matrix()
        #Boucler les ROIs auto et manuelle
        #Pour chaque ROI generer son mask 3D
        #ajouter ce masque 3D à un chanel 4D