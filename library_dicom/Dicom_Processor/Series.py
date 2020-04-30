from library_dicom.Dicom_Processor.Instance import Instance 
import os
#import glob
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



    def getSeriesDetails(self):
        """Read the first dicom in the folder and store Patient / Study / Series
        informations

        Returns:
            [dict] -- [Return the details of a Serie from the first Dicom]
        """
        seriesDetails = {}
        dataPatient = {}
        dataStudy = {}
        dataSeries = {}

        firstFileName = self.fileNames[0]
        dicomInstance = Instance(os.path.join(self.path,firstFileName))

        self.numberOfSlices = dicomInstance.getNumberOfSlices()
        self.sopClassUID = dicomInstance.getSOPClassUID()

        dataPatient["PatientID "] = dicomInstance.getPatientID()
        dataPatient["PatientName"] = dicomInstance.getPatientName()
        dataPatient["PatientBirthDate"] = dicomInstance.getPatientBirthDate()
        dataPatient["PatientSex"] = dicomInstance.getPatientSex()
        dataPatient["PatientWeight"] = dicomInstance.getPatientWeight()
        dataPatient["PatientHeight"] = dicomInstance.getPatientHeight()

        dataStudy["AccessionNumber"] = dicomInstance.getAccessionNumber()
        dataStudy["InstitutionName"] = dicomInstance.getInstitutionName()
        dataStudy["StudyDate"] = dicomInstance.getStudyDate()
        dataStudy["StudyDescription"] = dicomInstance.getStudyDescription()
        dataStudy["StudyID"] = dicomInstance.getStudyID()
        dataStudy["StudyInstanceUID"] = dicomInstance.getStudyInstanceUID()
        dataStudy["StudyTime"] = dicomInstance.getStudyTime()
        dataStudy["AcquisitionDate"] = dicomInstance.getAcquisitionDate()
        dataStudy["AcquisitionTime"] = dicomInstance.getAcquisitionTime()

        dataSeries["ImageOrientationPatient"] = dicomInstance.getImageOrientationPatient()
        dataSeries["Manufacturer"] = dicomInstance.getManufacturer()
        dataSeries["Modality"] = dicomInstance.getModality()
        dataSeries["SeriesName"] = dicomInstance.getSeriesName()
        dataSeries["SeriesDate"] = dicomInstance.getSeriesDate()
        dataSeries["SeriesDescription"] = dicomInstance.getSeriesDescription()
        dataSeries["SeriesInstanceUID"] = dicomInstance.getSeriesInstanceUID()
        dataSeries["SeriesNumber"] = dicomInstance.getSeriesNumber()
        dataSeries["SeriesTime"] = dicomInstance.getSeriesTime()

        seriesDetails["DataPatient"] = dataPatient
        seriesDetails["DataStudy"] = dataStudy
        seriesDetails["DataSeries"] = dataSeries

        if self.sopClassUID == '1.2.840.10008.5.1.4.1.1.128' : #TEP
            radioPharma = {}
            radioPharma["HalfLife"] = dicomInstance.getHalfLife()
            radioPharma["TotalDose"] = dicomInstance.getTotalDose()
            radioPharma["RadiopharmaceuticalStartDateTime"] = dicomInstance.getRadiopharmaceuticalStartDateTime()
            radioPharma["DecayCorrection"] = dicomInstance.getDecayCorrection()
            radioPharma["Unit"] = dicomInstance.getUnit()
            if dataSeries["Manufacturer"] == 'Philips' :
                radioPharma["ConversionSUV"] = dicomInstance.getConversionSUV()
                radioPharma["ConversionBQML"] = dicomInstance.getConversionBQML()

            seriesDetails["RadioPharma"] = radioPharma


        return (seriesDetails)
        

    def isSeriesValid(self):
        """Read all DICOMs in the current folder and check that all dicoms belong to the same series
        and number of instances mathing number of slice

        Returns:
            [bolean] -- [true if valid folder]
        """

        firstDicomDetails = self.getSeriesDetails()
        if self.numberOfSlices != len(self.fileNames):
            return False
        for fileName in self.fileNames:
            dicomInstance = Instance(os.path.join(self.path, fileName))

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
                return False
        return True

