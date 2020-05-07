import os
import numpy as np
import matplotlib.patches 

from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader

csv_reader = CsvReader('/home/salim/Bureau/11009101406003_apr 14_2010.csv')

#get manual ROI permet d'avoir le paragraphe des manual ROI
manual_rois = csv_reader.get_manual_rois()
print(manual_rois)
#Ligne par ligne tu peux recupérer un object qui decrit la ROI et que tu va pouvoir utiliser pour crée ta ROI
#print(csv_reader.convert_manual_row_to_object(manual_rois[0]))


def get_ROIS(manual_rois):
    ROIs = {}
    for i in range(csv_reader.number_of_manual_roi):
        ROIs[i+1] = csv_reader.convert_manual_row_to_object(manual_rois[i])
    number_of_roi = list(ROIs.keys())
    return ROIs, number_of_roi

ROIs , number_of_roi = get_ROIS(manual_rois) #pour avoir tous les rois dans un dict
#ROIs = { 1 : roi 1, 2: roi 2 etc}




#fonction pour mettre la liste des points en array N*2 pour matplotlib.patches.Polygon/Ellipse
def pointlist_to_pointarray (point_list):
    size = len(point_list)
    points = []
    for i in range(size):
        points.append(point_list[i].split())
    return np.asarray(points)


def create_closed_polygon(roi):
    points_array = pointlist_to_pointarray(roi['point_list']) #array nbr de points*2
    return matplotlib.patches.Polygon(points_array, closed = True)
    
    

def create_elipse(roi):
    points_array = pointlist_to_pointarray(roi['point_list'])
    width = abs(points_array[0][0] - points_array[1][0]) #centre_x - est_x 
    height = abs(points_array[0][1] - points_array[2][1]) #centre_y - nord_y
    return matplotlib.patches.Ellipse(points_array[0], width, height, angle =0)




#POUR ROI 1 

np_array_3D = np.zeros((256, 256, 700))



#dessiner le poly ou ellipse
#ecrire fonction pour dessiner soit poly soit ellipse pour chaque ROI 

def draw_patches(roi):
    if roi['type'] == 'Polygon' :
        return create_closed_polygon(roi)
    elif roi['type'] == 'Elipse' :
        return create_elipse(roi)



def min_max(roi): #return les min max des patches ellipse ou polygone
    if roi['type'] == 'Polygon' :
        points_array = pointlist_to_pointarray(roi['point_list'])
        x = []
        y= []
        for i in range (points_array.shape[0]):
            x.append(points_array[i, 0])
            y.append(points_array[i, 1])
        return min(x), min(y), max(x), max(y)
    
    elif roi['type'] == 'Elipse' :
        points_array = pointlist_to_pointarray(roi['point_list'])
        width = abs(points_array[0][0] - points_array[1][0]) #centre_x - est_x 
        height = abs(points_array[0][1] - points_array[2][1]) #centre_y - nord_y
        xmin = int(points_array[0][0] - width/2)
        ymin = int(points_array[0][1] - height/2)
        xmax = int(points_array[0][0] + width/2)
        ymax =  int(points_array[0][1] + height/2)
        return xmin, ymin, xmax, ymax


def mark_roi_in_slice(roi, slice, patch, number_of_roi): #patch = ellipse ou polygone #slice = np array 256*256
    xmin, ymin, xmax, ymax = min_max(roi)
    for i in range(xmin, xmax): 
        for j in range(ymin, ymax) : 
            if patch.contains_point([i,j], radius = 0) : #si vrai alors changement 
                slice[i,j] =  number_of_roi # = 1,2,3 etc 
    return slice 





#ROIs = dictionnaire de dictionnaire 
#boucle sur tous les ROIS du fichier 
for number_roi in number_of_roi : 
    patch = draw_patches(ROIs[number_roi])
    for number_of_slices in range(ROIs[number_roi]['first_slice'], ROIs[number_roi]['last_slice'] + 1 ) : 
        np_array_3D[number_of_slices] = mark_roi_in_slice(ROIs[number_roi], np_array_3D[number_of_slices], patch, number_roi) 



    
             







# Crée une NP array de taille arbitraire 256,256,700
# avec matplot lib creer un closed polygon et elipse qui correspond aux ROI qu'on a lue
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Polygon.html
# et une elipse si type elipse 
#https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Ellipse.html
# l'angle est toujours de 0  et tu a comme coordonée le pixel du centre, le pixel extremité est et pixel extremité nord
# donc en soustrayant les x de center/est et les Y de center/nord tu devrait avoir le width et height de l'elipse

#une fois que t'a le motif en 2D dans le plan axial tu duplique ce motif entre la first_slice et la last_slice
# sur ce volume tu met tous les pixel au numéro de la ROI (numéro arbitraire)
# pour chaque ROI je pense que tu va devoir ouvrir un channel dans ta numpy array ou tu mettra le masque de chaque ROI dans un chanel


#SK etape suivante
#superposer le mask avec un nifti  et visualisation
#check des valeurs par rapport a la partie resultat du CSV
#Gerer les CSV defini sur le plan coronal /saggital