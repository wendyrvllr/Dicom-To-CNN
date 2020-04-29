from library_dicom.Dicom_Processor.Instance import Instance 
import os
#import glob

class Series(object):

    def __init__(self, path):
        self.path = path
        self.fileNames = os.listdir(path) ##ici lister le contenu du repertoire avec os, liste
     

        #stocke la list des fichiers dans une variable fileNames
        #on boucle dessus
        #self.fileNames=['','']

    #Store commons data of Series in the current object
    def getSeriesDetails(self):
        firstFileName = self.fileNames[0] #on prend le premier fichier/dicom
        #dicomInstance = Instance(firstFileName)
        dicomInstance = Instance(os.path.join(self.path,firstFileName)) #join chemin série + 1er dicom
        self.patientID = dicomInstance.getPatientID()
        self.patientName = dicomInstance.getPatientName()
        self.studyInstanceUID = dicomInstance.getStudyInstanceUID()
        self.studyDescription = dicomInstance.getStudyDescription()
        self.acquisitionDate = dicomInstance.getAcquisitionDate()
        self.seriesInstanceUID = dicomInstance.getSeriesInstanceUID()
        self.seriesName = dicomInstance.getSeriesName()
        return (self.patientID, self.patientName, self.seriesInstanceUID, self.studyDescription,
                self.acquisitionDate, self.seriesInstanceUID, self.seriesName)
        
        ## ETC  => Patient ID, StudyInstanceUID, StudyDescription etc etc

    #cette methode va faire des check
    #elle va lire tous les fichier un a un grace à instance et elle va verifier
    #que tous les fichier ont le meme patientID
    #que tous les fichier ont la meme studyInstanceUID
    #que le nombre de fichier correspond au nombre de coupe déclaré dans le 1er dicom
    # retour un boolan vrai si tous les tests passent et faux sinon
    def isSeriesValid(self):
        for fileName in self.fileNames:
            #dicomInstance = Instance(fileName)
            dicomInstance = Instance(os.path.join(self.path, fileName))
            patientID = dicomInstance.getPatientID()
            patientName = dicomInstance.getPatientName()
            studyInstanceUID = dicomInstance.getStudyInstanceUID()
            studyDescription = dicomInstance.getStudyDescription()
            acquisitionDate = dicomInstance.getAcquisitionDate()
            seriesInstanceUID = dicomInstance.getSeriesInstanceUID()
            seriesName = dicomInstance.getSeriesName()
            if (self.patientID == patientID and
                self.patientName == patientName and
                self.studyInstanceUID == studyInstanceUID and
                self.studyDescription == studyDescription and
                self.acquisitionDate == acquisitionDate and
                self.seriesInstanceUID == seriesInstanceUID and
                self.seriesName == seriesName):
                return True
            else : 
                return False

            #ici a chaque tour de la boucle on verifie que ces parametre sont les meme que self.patientName... => sela suppose que getSeriesDetails soit executé avant


