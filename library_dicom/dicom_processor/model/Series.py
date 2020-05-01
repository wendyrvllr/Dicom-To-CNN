from library_dicom.dicom_processor.model.Instance import Instance
from library_dicom.dicom_processor.model.Modality import Modality
from library_dicom.dicom_processor.enums.TagEnum import *
from library_dicom.dicom_processor.model.NiftiBuilder import NiftiBuilder

import numpy as np
import os


class Series:
    """ A class representing a series Dicom
    """

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
        # SK AJOUTER RADIOPHARMACEUTICAL SI TEP
        return {
            'series' : series_details,
            'study' : study_details,
            'patient' : patient_details
        }
    """
    def is_series_valid(self):

        #SK : Ici il faut mieux tester l'egalité des dictionnaire plutot que de faire Item par Item

        firstDicomDetails = self.getSeriesDetails()

        if self.numberOfSlices != len(self.file_names):
            return False
        for fileName in self.file_names:
            dicomInstance = Instance(os.path.join(self.path, fileName), load_image=False)

            patientID = dicomInstance.getPatientID()
            patientName = dicomInstance.getPatientName()
            patientBirthDate = dicomInstance.getPatientBirthDate()
            patientSex = dicomInstance.getPatientSex()
            patientWeight = dicomInstance.getPatientWeight()
            patientHeight = dicomInstance.getPatientHeight()

            accessionNumber = dicomInstance.getAccessionNumber()
            institutionName = dicomInstance.getInstitutionName()
            studyDate = dicomInstance.getStudyDate()
            studyDescription = dicomInstance.getStudyDescription()
            studyID = dicomInstance.getStudyID()
            studyInstanceUID = dicomInstance.getStudyInstanceUID()
            studyTime = dicomInstance.getStudyTime()
            acquisitionDate = dicomInstance.getAcquisitionDate()
            acquisitionTime = dicomInstance.getAcquisitionTime()

            imageOrientationPatient = dicomInstance.getImageOrientationPatient()
            manufacturer = dicomInstance.getManufacturer()
            modality = dicomInstance.getModality()
            seriesName = dicomInstance.getSeriesName()
            seriesDate = dicomInstance.getSeriesDate()
            seriesDescription = dicomInstance.getSeriesDescription()
            seriesInstanceUID = dicomInstance.getSeriesInstanceUID()
            seriesNumber = dicomInstance.getSeriesNumber()
            seriesTime = dicomInstance.getSeriesTime()

            if (firstDicomDetails["DataPatient"]["PatientID"] != patientID or
                firstDicomDetails["DataPatient"]["PatientName"] != patientName or
                firstDicomDetails["DataPatient"]["PatientBirthDate"] != patientBirthDate or
                firstDicomDetails["DataPatient"]["PatientSex"] != patientSex or
                firstDicomDetails["DataPatient"]["PatientWeight"] != patientWeight or
                firstDicomDetails["DataPatient"]["PatientHeight"] != patientHeight or
                firstDicomDetails["DataStudy"]["AccessionNumber"] != accessionNumber or
                firstDicomDetails["DataStudy"]["InstitutionName"] != institutionName or
                firstDicomDetails["DataStudy"]["StudyDate"] != studyDate or
                firstDicomDetails["DataStudy"]["StudyDescription"] != studyDescription or
                firstDicomDetails["DataStudy"]["StudyID"] != studyID or
                firstDicomDetails["DataStudy"]["StudyInstanceUID"] != studyInstanceUID or
                firstDicomDetails["DataStudy"]["StudyTime"] != studyTime or
                firstDicomDetails["DataStudy"]["AcquisitionDate"] != acquisitionDate or
                firstDicomDetails["DataStudy"]["AcquisitionTime"] != acquisitionTime or
                firstDicomDetails["DataSeries"]["ImageOrientationPatient"] != imageOrientationPatient or
                firstDicomDetails["DataSeries"]["Manufacturer"] != manufacturer or
                firstDicomDetails["DataSeries"]["Modality"] != modality or
                firstDicomDetails["DataSeries"]["SeriesName"] != seriesName or
                firstDicomDetails["DataSeries"]["SeriesDate"] != seriesDate or
                firstDicomDetails["DataSeries"]["SeriesDescription"] != seriesDescription or
                firstDicomDetails["DataSeries"]["SeriesInstanceUID"] != seriesInstanceUID or
                firstDicomDetails["DataSeries"]["SeriesNumber"] != seriesNumber or
                firstDicomDetails["DataSeries"]["SeriesTime"] != seriesTime):

                if self.sopClassUID == '1.2.840.10008.5.1.4.1.1.128' : #TEP
                    radionuclideHalfLife = dicomInstance.getRadionuclideHalfLife()
                    radionuclideTotalDose = dicomInstance.getRadionuclideTotalDose()
                    radiopharmaceuticalStartDateTime= dicomInstance.getRadiopharmaceuticalStartDateTime()
                    decayCorrection = dicomInstance.getDecayCorrection()
                    units = dicomInstance.getUnits()
                    if (firstDicomDetails["RadioPharma"]["RadionuclideHalfLife"] != radionuclideHalfLife or
                        firstDicomDetails["RadioPharma"]["RadionuclideTotalDose"] != radionuclideTotalDose or
                        firstDicomDetails["RadioPharma"]["RadiopharmaceuticalStartDateTime"] != radiopharmaceuticalStartDateTime or
                        firstDicomDetails["RadioPharma"]["DecayCorrection"] != decayCorrection or
                        firstDicomDetails["RadioPharma"]["Units"] != units):
                        
                        
                        if firstDicomDetails["DataSeries"]["Manufacturer"] == 'Philips' :
                            conversionSUV = dicomInstance.getConversionSUV()
                            conversionBQML = dicomInstance.getConversionBQML()
                            if (firstDicomDetails["RadioPharma"]["ConversionSUV"] != conversionSUV or 
                                firstDicomDetails["RadioPharma"]["ConversionBQML"] != conversionBQML) : 
                                return False
                        return False
 
                return False
        return True
    """
    def get_numpy_array(self):
        if self.is_image_series == False : return
        instance_array = [Instance(file_name, load_image=True) for file_name in self.file_names]
        instance_array.sort(key=lambda x:int(instance_array.get_image_position()[2]), reverse=True)
        pixel_data = [instance.get_image_nparray() for instance in instance_array]
        np_array = np.stack(pixel_data,axis=0)
        self.instance_array = instance_array

        return np_array

    def export_nifti(self, file_path):
        nifti_builder = NiftiBuilder(self, file_path)
        nifti_builder.save_nifti()

