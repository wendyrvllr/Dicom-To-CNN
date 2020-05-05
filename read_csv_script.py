import os

from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader

csv_reader = CsvReader('/home/salim/Bureau/11009101406003_apr 14_2010.csv')

#get manual ROI permet d'avoir le paragraphe des manual ROI
manual_rois = csv_reader.get_manual_rois()
print(manual_rois)
#Ligne par ligne tu peux recupérer un object qui decrit la ROI et que tu va pouvoir utiliser pour crée ta ROI
print(csv_reader.convert_manual_row_to_object(manual_rois[0]))

#Maintenant
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
#Gerer les CSV defini sur le plan coronal / saggital