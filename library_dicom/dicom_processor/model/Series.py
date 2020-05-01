from library_dicom.dicom_processor.model.Instance import Instance
from library_dicom.dicom_processor.model.Modality import Modality
from library_dicom.dicom_processor.model.TagEnum import *
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
        self.fileNames = os.listdir(path) 

    def get_series_details(self):
        """Read the first dicom in the folder and store Patient / Study / Series
        informations

        Returns:
            [dict] -- [Return the details of a Serie from the first Dicom]
        """
        series_details = {}
        patient_details = {}
        study_details = {}

        firstFileName = self.fileNames[0]
        dicomInstance = Instance(os.path.join(self.path,firstFileName), load_image=False)

        series_details = dicomInstance.get_series_tags()
        patient_details = dicomInstance.get_patients_tags()
        study_details = dicomInstance.get_studies_tags()


        self.numberOfSlices = series_details[TagsSeries.NumberOfSlices.name]
        self.sopClassUID = dicomInstance.getSOPClassUID()

        print(dicomInstance.get_instance_tags())

        return {
            'series' : series_details,
            'study' : study_details,
            'patient' : patient_details
        }
        """
        seriesDetails["DataPatient"] = dataPatient
        seriesDetails["DataStudy"] = dataStudy
        seriesDetails["DataSeries"] = dataSeries

        if self.sopClassUID == Modality.PET :
            radioPharma = {}
            radioPharma["RadionuclideHalfLife"] = dicomInstance.getRadionuclideHalfLife()
            radioPharma["RadionuclideTotalDose"] = dicomInstance.getRadionuclideTotalDose()
            radioPharma["RadiopharmaceuticalStartDateTime"] = dicomInstance.getRadiopharmaceuticalStartDateTime()
            radioPharma["DecayCorrection"] = dicomInstance.getDecayCorrection()
            radioPharma["Units"] = dicomInstance.getUnits()
            if dataSeries["Manufacturer"] == 'Philips' :
                radioPharma["ConversionSUV"] = dicomInstance.getConversionSUV()
                radioPharma["ConversionBQML"] = dicomInstance.getConversionBQML()

            seriesDetails["RadioPharma"] = radioPharma

        *"""
        
    def is_series_valid(self):
        """Read all DICOMs in the current folder and check that all dicoms belong to the same series
        and number of instances mathing number of slice

        Returns:
            [bolean] -- [true if valid folder]
        """

        #SK : Ici il faut mieux tester l'egalité des dictionnaire plutot que de faire Item par Item

        firstDicomDetails = self.getSeriesDetails()

        if self.numberOfSlices != len(self.fileNames):
            return False
        for fileName in self.fileNames:
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

