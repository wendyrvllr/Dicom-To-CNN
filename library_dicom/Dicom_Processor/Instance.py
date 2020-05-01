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
        if 'SOPClassIUD' in self.dicomData.dir() : return self.dicomData.SOPClassUID
        else : return ("Undefined")

    def getNumberOfSlices(self):
        if 'NumberOfSlices' in self.dicomData.dir() : return self.dicomData.NumberOfSlices 
        else : return ("Undefined")

    def getPatientID(self): 
        if 'PatientID' in self.dicomData.dir(): return self.dicomData.PatientID
        else : return ("Undefined")
        
    def getPatientName(self):
        if 'PatientName' in self.dicomData.dir() : return self.dicomData.PatientName
        else : return ("Undefined")

    def getPatientBirthDate(self):
        if 'PatientBirthDate' in self.dicomData.dir() : return self.dicomData.PatientBirthDay
        else : return ("Undefined")

    def getPatientSex(self):
        if 'PatientSex' in self.dicomData.dir() : return self.dicomData.PatientSex
        else : return ("Undefined")

    def getPatientWeight(self):
        if 'PatientWeight' in self.dicomData.dir() : return self.dicomData.PatientWeight
        else : return ("Undefined")

    def getPatientHeight(self):
        if 'PatientHeight' in self.dicomData.dir() : return self.dicomData.PatientHeight
        else : return ("Undefined")

    def getAccessionNumber(self):
        if 'AccessioNumber' in self.dicomData.dir() : return self.dicomData.AccessionNumber
        else : return("Undefined")
    
    def getInstitutionName(self):
        if 'InstitutionName' in self.dicomData.dir() : return self.dicomData.InsitutionName
        else : return ("Undefined")

    def getStudyDate(self):
        if 'StudyDate' in self.dicomData.dir() : return self.dicomData.StudyDate
        else : return ("Undefined")

    def getStudyDescription(self):
        if 'StudyDescription' in self.dicomData.dir() : return self.dicomData.StudyDescription
        else : return ("Undefined")

    def getStudyID(self):
        if 'Study ID' in self.dicomData.dir() : return self.dicomData.StudyID
        else : return("Undefined")

    def getStudyInstanceUID(self):
        if 'StudyInstance' in self.dicomData.dir() : return self.dicomData.StudyInstanceUID
        else : return("Undefined")

    def getStudyTime(self):
        if 'StudyTime' in self.dicomData.dir() : return self.dicomData.StudyTime
        else : return ("Undefined")

    def getAcquisitionDate(self):
        if 'AcquisitionDate' in self.dicomData.dir() : return self.dicomData.AcquisitionDate
        else : return ("Undefined")
    
    def getAcquisitionTime(self):
        if 'AcquisitionTime' in self.dicomData.dir() : return self.dicomData.AcquisitionTime 
        else : return ("Undefined")

    def getImageOrientationPatient(self):
        if 'ImageOrientationPatient' in self.dicomData.dir() : return self.dicomData.ImageOrientationPatient 
        else : return ("Undefined")

    def getManufacturer(self):
        if 'Manufacturer' in self.dicomData.dir() : return self.dicomData.Manufacturer
        else : return ("Undefined")

    def getModality(self):
        if 'Modality' in self.dicomData.dir() : return self.dicomData.Modality
        else : return ("Undefined")

    def getSeriesName(self):
        if 'SeriesName' in self.dicomData.dir() : return self.dicomData.SeriesName
        else : return ("Undefined")

    def getSeriesDate(self):
        if 'SeriesDate' in self.dicomData.dir() : return self.dicomData.SeriesDate 
        else : return ("Undefined")

    def getSeriesDescription(self):
        if 'SeriesDescription' in self.dicomData.dir() : return self.dicomData.SeriesDescription 
        else : return ("Undefined")

    def getSeriesInstanceUID(self):
        if 'SeriesInstanceUID' in self.dicomData.dir() : return self.dicomData.SeriesInstanceUID
        else : return ("Undefined")

    def getSeriesNumber(self):
        if 'SeriesNumber' in self.dicomData.dir() : return self.dicomData.SeriesNumber
        else : return ("Undefined")

    def getSeriesTime(self):
        if 'SeriesTime' in self.dicomData.dir() : return self.dicomData.SeriesTime 
        else : return ("Undefined")

    #pour TEP


    def getRadionuclideHalfLife(self):
        if 'RadionuclideHalfLife' in self.dicomData.dir() : return self.dicomData.RadionuclideHalfLife
        else : return ("Undefined")

    def getRadionuclideTotalDose(self):
        if 'TotalDose' in self.dicomData.dir() : return self.dicomData.RadionuclideTotalDose
        else : return ("Undefined")

    def getRadiopharmaceuticalStartDateTime(self):
        if 'RadiopharmaceuticalStartDateTime' in self.dicomData.dir() : return self.dicomData.RadiopharmaceuticalStartDateTime
        else : return ("Undefined")

    def getDecayCorrection(self):
        if 'DecayCorrection' in self.dicomData.dir() : return self.dicomData.DecayCorrection
        else : return ("Undefined")

    def getUnits(self):
        if 'Units' in self.dicomData.dir() :  return self.dicomData.Units
        else : return ("Undefined")

#Problème pour afficher les tags privés : 
#7053 1000 : SUV Scale Factor
#7053 1009 : Activity Concentration Scale Factor
    def getConversionSUV(self):
        if '0x70531000' in self.dicomData : return self.dicomData[0x70531000].value
        else : return ("Undefined")

    def getConversionBQML(self):
        if '0x70531009' in self.dicomData : return self.dicomData[0x70531009].value
        else : return ("Undefined")

    
    