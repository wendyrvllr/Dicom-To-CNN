import os
import numpy as np
import matplotlib.patches 

from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader

csv_reader = CsvReader('/home/salim/Bureau/11009101406003_apr 14_2010.csv')

#get manual ROI permet d'avoir le paragraphe des manual ROI
manual_rois = csv_reader.get_manual_rois()



def get_manual_ROIS(manual_rois):
    ROIs = {}
    for i in range(csv_reader.number_of_manual_roi):
        ROIs[i+1] = csv_reader.convert_manual_row_to_object(manual_rois[i])
    number_of_roi = list(ROIs.keys())
    return ROIs, number_of_roi

ROIs , number_of_roi = get_manual_ROIS(manual_rois) #pour avoir tous les rois dans un dict
#ROIs = { 1 : roi 1, 2: roi 2 etc}




#fonction pour mettre la liste des points en array N*2 pour matplotlib.patches.Polygon/Ellipse
#met les points nifti en array [ [x,y,slice] , [x ,y, slice], ...]
def pointlist_to_pointarray (point_list):
    size = len(point_list)
    points = []
    for i in range(size):
        points.append(point_list[i].split())
    return np.asarray(points)

#POUR ROIS

def create_closed_polygon(roi):
    points_array = pointlist_to_pointarray(roi['point_list']) #array nbr de points*2
    return matplotlib.patches.Polygon(points_array, closed = True)
    
    

def create_elipse(roi):
    points_array = pointlist_to_pointarray(roi['point_list'])
    width = abs(points_array[0][0] - points_array[1][0]) #centre_x - est_x 
    height = abs(points_array[0][1] - points_array[2][1]) #centre_y - nord_y
    return matplotlib.patches.Ellipse(points_array[0], width, height, angle =0)





#dessiner le polygone ou ellipse axial/coronal/sagittal

def draw_patches(roi):
    if (roi['type'] == 'Polygon' or roi['type'] == 'Polygon_Coronal' or roi['type'] == 'Polygon_Sagittal') :
        return create_closed_polygon(roi)
    elif (roi['type'] == 'Elipse' or roi['type'] == 'Elipse_Coronal' or roi['type'] == 'Elipse_Sagittal') :
        return create_elipse(roi)



def min_max(roi): #return les min max des patches ellipse ou polygone
    if (roi['type'] == 'Polygon' or roi['type'] == 'Polygon_Coronal' or roi['type'] == 'Polygon_Sagittal') :
        points_array = pointlist_to_pointarray(roi['point_list'])
        x = []
        y= []
        for i in range (points_array.shape[0]):
            x.append(points_array[i, 0])
            y.append(points_array[i, 1])
        return min(x), min(y), max(x), max(y)
    
    elif (roi['type'] == 'Elipse' or roi['type'] == 'Elipse_Coronal' or roi['type'] == 'Elipse_Sagittal') :
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



np_array_4D = []

#ROIs = dictionnaire de dictionnaire 
#boucle sur tous les ROIS du fichier 
for number_roi in number_of_roi : # 1 2 3 4 
    patch = draw_patches(ROIs[number_roi])
    np_array_3D = np.zeros((256, 256, 700))

    for number_of_slices in range(ROIs[number_roi]['first_slice'], ROIs[number_roi]['last_slice'] + 1 ) : 
        np_array_3D[number_of_slices] = mark_roi_in_slice(ROIs[number_roi], np_array_3D[number_of_slices], patch, number_roi) 
        
        if (ROIs[number_roi]['type'] == 'Polygon_Coronal' or ROIs[number_roi]['type'] == 'Elipse_Coronal') : 
            np_array_3D = change_repere(ROIs[number_roi], np_array_3D)
        elif (ROIs[number_roi]['type'] == 'Polygon_Sagittal' or ROIs[number_roi]['type'] == 'Elipse_Sagittal') :
            np_array_3D = change_repere(ROIs[number_roi], np_array_3D)



    np_array_4D.append( np_array_3D) #cube 0 1 2 3 pour 4 ROIs

np.asarray(np_array_4D)


#POUR TRAITEMENT CORRONAL ET SAGITTAL
# 

def change_repere(roi, np_array_3D):
    if (roi['type'] == 'Polygon_Coronal' or roi['type'] == 'Elipse_Coronal') :
        return coronal_to_axial(np_array_3D)
    elif (roi['type'] == 'Polygon_Sagittal' or roi['type'] == 'Elipse_Sagittal'):
        return sagittal_to_axial(np_array_3D)


def coronal_to_axial(np_array_3D):
    return np.transpose(np_array_3D, (1,2,0)) #coronnal x y z -> axial y z x 

def sagittal_to_axial(np_array_3D):
    return np.transpose(np_array_3D, (2,0,1)) #sagittal x y z - > axial  z x y 





#Pour NIFTI ROIs

csv_reader = CsvReader('/home/salim/Bureau/11009101406003_apr 14_2010_NIFTI.csv')

#get manual ROI permet d'avoir le paragraphe des manual ROI
nifti_rois = csv_reader.get_nifti_rois()

def get_nifti_ROIS(manual_rois):
    ROIs = {}
    for i in range(csv_reader.number_of_nifti_roi):
        ROIs[i+1] = csv_reader.convert_nifti_row_to_list_point(nifti_rois[i])
    number_of_roi = list(ROIs.keys())
    return ROIs, number_of_roi

ROIs_nifti , number_of_nifti_roi = get_nifti_ROIS(nifti_rois) #pour avoir tous les rois dans un dict
#ROIs = { 1 : roi 1(liste de points), 2: roi 2(liste de points) etc}

np_array_nifti_4D = []

for number_nifti_roi in number_of_nifti_roi : 
    liste_nifti_points = pointlist_to_pointarray(ROIs_nifti[number_nifti_roi]) #liste de points pour chaque ROIS
    np_array_nifti_3D = np.zeros((256, 256, 700)) 
    for points in liste_nifti_points :
        np_array_nifti_3D[points[2]][points[0], points[1]] = number_nifti_roi #1 pour ROi 1, 2 pour ROI 2 


    np_array_nifti_4D.append( np_array_nifti_3D )

np.asarray(np_array_nifti_4D)




#SK etape suivante
#superposer le mask avec un nifti  et visualisation
#check des valeurs par rapport a la partie resultat du CSV