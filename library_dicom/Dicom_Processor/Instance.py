import pydicom
import os


class Instance:

    def __init__(self, path):
        self.path = path
        self.dicomData = pydicom.dcmread(path) #read dicom 

    def getPatientID(self): 
        return self.dicomData.PatientID
        
    def getPatientName(self):
        return self.dicomData.PatientName
    
    def getStudyInstanceUID(self):
        return self.dicomData.StudyInstanceUID

    def getStudyDescription(self):
        return self.dicomData.StudyDescription

    def getAcquisitionDate(self):
        return self.dicomData.AcquisitionDate

    def getSeriesInstanceUID(self):
        return self.dicomData.SeriesInstanceUID

    def getSeriesName(self):
        return self.dicomData.SeriesName
    