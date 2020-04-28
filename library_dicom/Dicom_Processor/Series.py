import library_dicom.Dicom_Processor.Instance import Instance 

class Series(object):

    def __init__(path):
        self.path = path
        #ici lister le contenu du repertoire avec os
        #stocke la list des fichiers dans une variable filename
        #on boucle dessus
        self.fileNames=['','']

    #Store commons data of Series in the current object
    def getSeriesDetails():
        firstFileName = self.fileName[0]
        dicomInstance = new Instance(firstFileName)
        self patientName = dicomInstance.getPatientName()
        
        ## ETC  => Patient ID, StudyInstanceUID, StudyDescription etc etc

    #cette methode va faire des check
    #elle va lire tous les fichier un a un grace à instance et elle va verifier
    #que tous les fichier ont le meme patientID
    #que tous les fichier ont la meme studyInstanceUID
    #que le nombre de fichier correspond au nombre de coupe déclaré dans le 1er dicom
    # retour un boolan vrai si tous les tests passent et faux sinon
    def isSeriesValid():
        for fileName in self.fileNames:
            dicomInstance = new Instance(fileName)
            seriesInstanceUID = dicomInstance.getSeriesInstanceUID()
            #ici a chaque tour de la boucle on verifie que ces parametre sont les meme que self.patientName... => sela suppose que getSeriesDetails soit executé avant


