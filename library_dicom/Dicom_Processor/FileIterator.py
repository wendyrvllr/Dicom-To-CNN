from library_dicom.Dicom_Processor.Series import Series
import os

#list of Series path
def getSeriesPath(path):
    seriesPath = []
    for (path, dirs, files) in os.walk(path): #os.walk parcoure tout le repertoire
        if not (dirs) :  #si pas de sous dossiers = .dcm
            seriesPath.append(path) #on récupère le path qu'on range dans la liste
    return seriesPath #return une liste avec tous les chemins de toute les séries de tout le repertoire


seriesPaths = getSeriesPath('/repertoire')

dicom1 = Series(seriesPaths[0]) #chemin de la premiere série
seriesInfo= dicom1.getSeriesDetails()
#SK OK pas mal tu peux maintenant essayer de boucler sur les series que tu trouve, checker leur contenu et remplir une variable
# qui va contenir un "abre" avec l'ID patient, en clé 1ere, les details du patient (nom) et un array de studies avec comme clé 1er leur series InstanceUID et leurs details puis une array de series
print(seriesInfo)
print(dicom1.isSeriesValid()) #test

#Ici on va faire un script