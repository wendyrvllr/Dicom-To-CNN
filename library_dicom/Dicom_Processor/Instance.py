import pydicom
import os


class Instance:
    """A class to represent a Dicom file 
    """

    def __init__(self, path):
        """Construct a Dicom file object

        Arguments:
            path {[String]} -- [Absolute path where the Dicom file is located]
        """
        self.path = path
        self.dicomData = pydicom.dcmread(path) 

    def getSOPClassUID(self):
        return self.dicomData.SOPClassUID

    def getNumberOfSlices(self):
        return self.dicomData.NumberOfSlices 

    def getPatientID(self): 
        return self.dicomData.PatientID
        
    def getPatientName(self):
        return self.dicomData.PatientName

    def getPatientBirthDate(self):
        return self.dicomData.PatientBirthDay

    def getPatientSex(self):
        return self.dicomData.PatientSex

    def getPatientWeight(self):
        return self.dicomData.PatientWeight

    def getPatientHeight(self):
        return self.dicomData.PatientHeight

    def getAccessionNumber(self):
        return self.dicomData.AccessionNumber
    
    def getInstitutionName(self):
        return self.dicomData.InsitutionName 

    def getStudyDate(self):
        return self.dicomData.StudyDate

    def getStudyDescription(self):
        return self.dicomData.StudyDescription

    def getStudyID(self):
        return self.dicomData.StudyID

    def getStudyInstanceUID(self):
        return self.dicomData.StudyInstanceUID

    def getStudyTime(self):
        return self.dicomData.StudyTime

    def getAcquisitionDate(self):
        return self.dicomData.AcquisitionDate
    
    def getAcquisitionTime(self):
        return self.dicomData.AcquisitionTime 

    def getImageOrientationPatient(self):
        return self.dicomData.ImageOrientationPatient 

    def getManufacturer(self):
        return self.dicomData.Manufacturer

    def getModality(self):
        return self.dicomData.Modality

    def getSeriesName(self):
        return self.dicomData.SeriesName

    def getSeriesDate(self):
        return self.dicomData.SeriesDate 

    def getSeriesDescription(self):
        return self.dicomData.SeriesDescription 

    def getSeriesInstanceUID(self):
        return self.dicomData.SeriesInstanceUID

    def getSeriesNumber(self):
        return self.dicomData.SeriesNumber

    def getSeriesTime(self):
        return self.dicomData.SeriesTime 

    #pour TEP


    def getHalfLife(self):
        return self.dicomData[0x00181075].value

    def getTotalDose(self):
        return self.dicomData[0x00181074].value

    def getRadiopharmaceuticalStartDateTime(self):
        return self.dicomData[0x00181078].value

    def getDecayCorrection(self):
        return self.dicomData[0x00541102].value
    
    def getUnit(self):
        return self.dicomData[0x00541001].value

    def getConversionSUV(self):
        return self.dicomData[0x70531000].value

    def getConversionBQML(self):
        return self.dicomData[0x70531009].value

    
    