import pydicom
import os

from library_dicom.dicom_processor.enums.TagEnum import *
from library_dicom.dicom_processor.enums.SopClassUID import *

class Instance:
    """A class to represent a Dicom file 
    """

    def __init__(self, path, load_image=True):
        """Construct a Dicom file object

        Arguments:
            path {[String]} -- [Absolute path where the Dicom file is located]
        """
        self.path = path
        if (load_image) : self.__load_full_instance()
        else : self.__load_metadata()

    #SK : le double __ est pour signaler que que cette methode est "privée" elle n'es sencée etre utilisée que par la class elle meme
    # J'ai mis deux methode de l'ecture defini dans constructeur, si on ne veut que les metadonées ou non
    def __load_metadata(self):
        self.dicomData = pydicom.dcmread(self.path, stop_before_pixels=True)
    
    def __load_full_instance(self):
        self.dicomData = pydicom.dcmread(self.path)

    #SK : Au lieu de copier tous les tags, je les ai lister dans une enumeration et je boucle dessus
    # ca permettra d'ajouter ou d'enlever facilement les tags dans l'enum
    def get_series_tags(self):
        series_tags={}
        for tag_address in TagsSeries:
            if tag_address.value in self.dicomData : series_tags[tag_address.name] = self.dicomData[tag_address.value].value
            else : series_tags[tag_address.name] = "Undefined"
        return series_tags

    def get_patients_tags(self):
        patient_tags={}
        for tag_address in TagsPatient:
            if tag_address.value in self.dicomData : patient_tags[tag_address.name] = self.dicomData[tag_address.value].value
            else : patient_tags[tag_address.name] = "Undefined"
        return patient_tags

    def get_studies_tags(self):
        studies_tags={}
        for tag_address in TagsStudy:
            if tag_address.value in self.dicomData : studies_tags[tag_address.name] = self.dicomData[tag_address.value].value
            else : studies_tags[tag_address.name] = "Undefined"
        return studies_tags

    def get_instance_tags(self):
        instance_tags={}
        for tag_address in TagsInstance:
            if tag_address.value in self.dicomData : instance_tags[tag_address.name] = self.dicomData[tag_address.value].value
            else : instance_tags[tag_address.name] = "Undefined"
        return instance_tags

    #SK : Le SOPClassUID est une clé obligatoire dans le DICOM si elle n'est pas présente je déclanche une exception
    #Cette exeception doit etre gérée la ou elle est appellée sinon le programme va s'arreter
    #Ici j'ai pas fait de catch, normalement elle ne doit jamais etre absente
    def get_sop_class_uid(self):
        if 'SOPClassUID' in self.dicomData.dir() : return self.dicomData.SOPClassUID
        else : raise Exception('Undefined SOP Class UID')

    def get_radiopharmaceuticals_tags(self):
        radiopharmaceuticals_tags={}
        radiopharmaceutical_sequence = []

        try :
            radiopharmaceutical_sequence = self.dicomData[0x00540016][0]
        except Exception: 
            print("no Radiopharmaceuticals tags")

        for tag_address in TagsRadioPharmaceuticals:
            if tag_address.value in radiopharmaceutical_sequence : radiopharmaceuticals_tags[tag_address.name] = radiopharmaceutical_sequence[tag_address.value].value
            else : radiopharmaceuticals_tags[tag_address.name] = "Undefined"

        return radiopharmaceuticals_tags

    #SK Le return est coté en condition ternaire
    def is_secondary_capture(self):
        return True if self.getSOPClassUID in CapturesSOPClass else False
    
    