from library_dicom.Dicom_Processor.Series import Series
import os

#Series path
def getSeriesPath(path):
    seriesPath = []
    for (path, dirs, files) in os.walk(path): #os.walk parcoure tout le repertoire
        if not (dirs) :  #si pas de sous dossiers = .dcm
            seriesPath.append(path) #on récupère le path qu'on range dans la liste
    return seriesPath #return une liste avec tous les chemins de toute les séries de tout le repertoire


seriesPaths = getSeriesPath('/repertoire')

dicom1 = Series(seriesPaths[0]) 
seriesInfo= dicom1.getSeriesDetails()
print(seriesInfo)
print(dicom1.isSeriesValid())


#print de seriesInfo
#Ici on va faire un script