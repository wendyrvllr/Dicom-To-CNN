import pydicom
import os


class Instance(object):

    def __init__(self, path):
        self.path = path
        self dicomData = pydicom.dcmread(path)

    def getPatientID():
    def getPatientName():
        return self.dicomData.PatientName
    
    def getStudyInstanceUID():
    def getStudyDescription():
    def getAcquisitionDate():
    def getSeriesInstanceUID():
    def getSeriesName():
    