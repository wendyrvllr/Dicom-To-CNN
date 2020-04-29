from library_dicom.Dicom_Processor.Series import Series
import os

#Series path
def seriesPath(path):
    for (path, dirs, files) in os.walk(path): #os.walk parcour tout le repertoire
        print (path)
        print (dirs)
        print (files)
        print ("----")
        #quand files = .dcm, prendre path correspondant -> pour instancier Series





dicom1 = Series('/monchemin')
seriesInfo= dicom1.getSeriesDetails()
print(seriesInfo)
print(dicom1.isSeriesValid())


#print de seriesInfo
#Ici on va faire un script