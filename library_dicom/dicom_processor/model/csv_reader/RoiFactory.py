"""
Cette classe va servir à parser le dictionnaire ROI et instancier le bon objet ROI
Set la taille de la matrice Image
Superposer la matrice image et masque pour les metrics ? => Peut etre pas
"""
class RoiFactory():

    def __init__(self, details, image_dimension):
       self.details = details
       self.image_dimension = image_dimension
    
    def read_roi(self):
        if (self.details['type_number'] == 1):
            result_answer['type'] = 'Polygon'

        elif (self.details['type_number'] == 11):
            result_answer['type'] = 'Elipse'

        elif (self.details['type_number'] == 2):
            result_answer['type'] = 'Polygon_Coronal'

        elif (self.details['type_number'] == 12):
            result_answer['type'] = 'Elipse_Coronal'

        elif (self.details['type_number'] == 3):
            result_answer['type'] = 'Polygon_Sagittal'

        elif (self.details['type_number'] == 13):
            result_answer['type'] = 'Elipse_Coronal'


    