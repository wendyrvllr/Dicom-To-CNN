import numpy as np
import os

from Instance import Instance
from Modality import *
from NiftiBuilder import NiftiBuilder

from library_dicom.dicom_processor.enums.TagEnum import *
from library_dicom.dicom_processor.enums.SopClassUID import *

class Series():
    """ A class representing a series Dicom
    """
    @classmethod
    def get_series_object(cls, path):
        first_file_name = os.listdir(path)[0]
        first_instance = Instance( os.path.join(path,first_file_name) )
        sop_class_uid = first_instance.get_sop_class_uid()
        if(sop_class_uid == ImageModalitiesSOPClass.PT.value or sop_class_uid == ImageModalitiesSOPClass.EnhancedPT.value):
            from SeriesPT import SeriesPT
            return SeriesPT(path)
        else : return Series(path)
    
    def __init__(self, path):
        """Construct a Dicom Series Object

        Arguments:
            path {String} -- [Absolute Path where Dicom Series is located (hirachical Dicoms)]
        """

        self.path = path
        self.file_names = os.listdir(path) 

    def get_series_details(self):
        """Read the first dicom in the folder and store Patient / Study / Series
        informations

        Returns:
            [dict] -- [Return the details of a Serie from the first Dicom]
        """
        self.series_details = {}
        self.patient_details = {}
        self.study_details = {}

        firstFileName = self.file_names[0]
        dicomInstance = Instance(os.path.join(self.path,firstFileName), load_image=True)

        self.series_details = dicomInstance.get_series_tags()
        self.patient_details = dicomInstance.get_patients_tags()
        self.study_details = dicomInstance.get_studies_tags()
        self.sop_class_uid = dicomInstance.get_sop_class_uid()
        self.is_image_series = dicomInstance.is_image_modality()

        if dicomInstance.get_sop_class_uid == '1.2.840.10008.5.1.4.1.1.128' or dicomInstance.get_sop_class_uid == '1.2.840.10008.5.1.4.1.1.130' : #TEP  
            self.radiopharmaceutical_details = {}
            self.radiopharmaceutical_details = dicomInstance.get_radiopharmaceuticals_tags()
            return {
                'series' : self.series_details,
                'study' : self.study_details,
                'patient' : self.patient_details, 
                'radiopharmaceutical' : self.radiopharmaceutical_details
            }

        return {
            'series' : self.series_details,
            'study' : self.study_details,
            'patient' : self.patient_details
        }
    
    def is_series_valid(self):

        #SK : Ici il faut mieux tester l'egalite des dictionnaire plutot que de faire Item par Item

        firstDicomDetails = self.get_series_details()

        if firstDicomDetails['series']['NumberOfSlices'] != len(self.file_names):
            return False
        for fileName in self.file_names:
            dicomInstance = Instance(os.path.join(self.path, fileName), load_image=False)
            if (dicomInstance.get_series_tags != firstDicomDetails['series'] or
                dicomInstance.get_patients_tags != firstDicomDetails['patient'] or
                dicomInstance.get_studies_tags != firstDicomDetails['study']):
                if dicomInstance.get_sop_class_uid == '1.2.840.10008.5.1.4.1.1.128' or dicomInstance.get_sop_class_uid == '1.2.840.10008.5.1.4.1.1.130' :
                    if dicomInstance.get_radiopharmaceuticals_tags != firstDicomDetails['radiopharmaceutical']:
                        return False
            return False
        return True
            
        
    
    def get_numpy_array(self):
        if self.is_image_series == False : return
        instance_array = [Instance(os.path.join(self.path, file_name), load_image=True) for file_name in self.file_names]
        instance_array.sort(key=lambda instance_array:int(instance_array.get_image_position()[2]), reverse=True)
        pixel_data = [instance.get_image_nparray() for instance in instance_array]
        np_array = np.stack(pixel_data,axis=0)
        self.instance_array = instance_array

        return np_array

    def get_z_spacing(self):
        """ called by __getMetadata """
        Z_positions = [ instance.get_image_position()[2] for instance in self.instance_array ]
        
        initial_z_spacing = Z_positions[0]-Z_positions[1]
        for i in range(1,len(Z_positions)):
            z_spacing = Z_positions[i-1]-Z_positions[i]
            if (z_spacing!=initial_z_spacing):
                raise Exception('Unconstant Spacing')
        return initial_z_spacing

    #check origin direction spacing de nifti

    def export_nifti(self, file_path):
        nifti_builder = NiftiBuilder(self)
        nifti_builder.save_nifti(file_path)

