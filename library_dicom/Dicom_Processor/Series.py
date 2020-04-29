from library_dicom.Dicom_Processor.Instance import Instance 
import os
#import glob
#SK : Je viens de voir que depuis python 3 y pas besoin d'hériter de object pour chaque class (c'est auto)
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
            [type] -- [description]
        """

        firstFileName = self.fileNames[0]
        dicomInstance = Instance(os.path.join(self.path,firstFileName)) #join series path and 1st dicom
        self.patientID = dicomInstance.getPatientID()
        self.patientName = dicomInstance.getPatientName()
        self.studyInstanceUID = dicomInstance.getStudyInstanceUID()
        self.studyDescription = dicomInstance.getStudyDescription()
        self.acquisitionDate = dicomInstance.getAcquisitionDate()
        self.seriesInstanceUID = dicomInstance.getSeriesInstanceUID()
        self.seriesName = dicomInstance.getSeriesName()

        # SK : Ici a voir si il faut peut etre pas mettre toutes ces infos dans un dictionnaire et ne retourner que le dictionnaire
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
        """Read all DICOMs in the current folder and check that all dicoms belong to the same series
        and number of instances mathing number of slice

        Returns:
            [bolean] -- [true if valid folder]
        """

        #SK : pour l'algorithmie, ici tu est dans un boucle, si tu fait un return
        # toute la methode est intérompue, si tu fait "si toute les conditions sont egale return true"
        # alors tu va tester le 1er fichier de la liste et c'est fini t'a fonction retourne true est c'es tout.
        #Donc j'ai changé au lieu de l'égalité je cherche une difference, si y a une difference je return false
        # ce qui me permet de pas avoir à lire tous les fichiers dans ce cas, je sais qu'il y en a un qui ne va pas
        # donc je retourne false
        # si la boucle se termine sans avoir rendu de false alors en dehors de la boucle j'ai un return true qui permet 
        # de renvoyer true quand la boucle s'est bien terminée sans recontrer de soucis

        #SK2 : Ici il nous manque un check sur le nombre de slice, il faut checker que le nombre de slice dans le 1er dicom
        # est bien égal au nombre de fichier qu'on a dans le repertoire 
        # donc dans le get series detail il faut stocker dans cet objet le valeur du tag 0054,0081 (number of slice)
        # y a un utilitaire dans pydicom pour retrouve le nom de l'element a partir du code 
        #https://pydicom.github.io/pydicom/dev/reference/datadict.html
        #donc avant la boucle faudrait un if qui check que le nombre de fichier dans le repertoire est égale au nomber of slice
        # si c'est pas egale on return false sans rentrer dans la boucle
        for fileName in self.fileNames:
            dicomInstance = Instance(os.path.join(self.path, fileName))
            patientID = dicomInstance.getPatientID()
            patientName = dicomInstance.getPatientName()
            studyInstanceUID = dicomInstance.getStudyInstanceUID()
            studyDescription = dicomInstance.getStudyDescription()
            acquisitionDate = dicomInstance.getAcquisitionDate()
            seriesInstanceUID = dicomInstance.getSeriesInstanceUID()
            seriesName = dicomInstance.getSeriesName()
            if (self.patientID != patientID or
                self.patientName != patientName or
                self.studyInstanceUID != studyInstanceUID or
                self.studyDescription != studyDescription or
                self.acquisitionDate != acquisitionDate or
                self.seriesInstanceUID != seriesInstanceUID or
                self.seriesName != seriesName):
                return False
        #if loop ended without non mathing element return true 
        return True

