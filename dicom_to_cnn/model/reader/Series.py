import numpy as np
import os
from os.path import basename,splitext
import SimpleITK as sitk 

from dicom_to_cnn.model.reader.Instance import Instance
from dicom_to_cnn.enums.TagEnum import *
from dicom_to_cnn.enums.SopClassUID import *

class Series():
    """ A class representing a series Dicom
    """
    
    def __init__(self, path:str):
        """Construct a Dicom Series Object

        Arguments:
            path {str} -- [Absolute Path where Dicom Series is located (hirachical Dicoms)]
        """

        self.path = path
        self.file_names = os.listdir(path)
        self.number_of_files = len(self.file_names)

    def get_number_of_files(self) -> int:
        """method to get number of instance in serie folder

        Returns:
            [int]: [return number of files/instances in serie folder]
        """
        return self.number_of_files
    
    def get_first_instance_metadata(self) -> Instance:
        """method to read the first dicom instance in the folder

        Returns:
            [Instance]: [return Instance object]
        """
        firstFileName = self.file_names[0]
        return Instance(os.path.join(self.path,firstFileName), load_image=True)


    def get_series_details(self) -> dict:
        """Read the first dicom in the folder and store Patient / Study / Series
        informations

        Returns:
            [dict] -- [Return the details of a Serie from the first Dicom]
        """
        self.series_details = {}
        self.patient_details = {}
        self.study_details = {}

        dicomInstance = self.get_first_instance_metadata()

        self.series_details = dicomInstance.get_series_tags()
        self.patient_details = dicomInstance.get_patients_tags()
        self.study_details = dicomInstance.get_studies_tags()
        self.instance_details = dicomInstance.get_instance_tags()
        self.sop_class_uid = dicomInstance.get_sop_class_uid()
        self.is_image_series = dicomInstance.is_image_modality()

        return {
            'series' : self.series_details,
            'study' : self.study_details,
            'patient' : self.patient_details,
            'path' : self.path,
            'files' : self.number_of_files,
            'instance' : self.instance_details
        }

    def is_series_valid(self) -> bool:
        """check if the number of slice is wrong, or if the Series Instance UID is the same

        Returns:
            [bool]: [description]
        """
        firstDicomDetails = self.get_series_details()
        #Le tag number of slice n'est que pour PT et NM, pas trouvé d'autre tag fiable pour les autres series
        if firstDicomDetails['series']['NumberOfSlices']!="Undefined" and firstDicomDetails['series']['NumberOfSlices'] != len(self.file_names):
            print('wrong number of slice')
            return False

        for fileName in self.file_names:
            dicomInstance = Instance(os.path.join(self.path, fileName), load_image=False)
            if (dicomInstance.get_series_tags()['SeriesInstanceUID'] != firstDicomDetails['series']['SeriesInstanceUID']):
                print('Not same Series Instance UID')
                return False
        
        return True
        
    def is_image_modality(self) -> bool :
        """check if SOPClassUID from the first dicom is in sop values list

        Returns:
            [type]: [description]
        """
        return self.get_first_instance_metadata().is_image_modality()

    def is_primary_image(self) -> bool :
        """check if "PRIMARY" in ImageType tag values

        Returns:
            [bool]: [description]
        """
        return ( "PRIMARY" in self.series_details['ImageType'])

    def is_localizer_series(self) -> bool :
        """check if "LOCALIZER" in ImageType tag values

        Returns:
            [bool]: [description]
        """
        return ( "LOCALIZER" in self.series_details['ImageType'])

    def get_instances_ordered(self) -> list:
        """function to sort instances array by z positions

        Returns:
            [list]: [return ordered instance array]
        """
        instance_array = [Instance(os.path.join(self.path, file_name), load_image=True) for file_name in self.file_names]
        instance_array.sort(key=lambda instance_array:int(instance_array.get_image_position()[2]))
        self.instance_array = instance_array
        return instance_array 


    def get_numpy_array(self) -> np.ndarray:
        """method to get 3d numpy array of the serie 

        Returns:
            [ndarray]: [return ndarray of series]
        """
        if self.is_image_modality == False : return

        pixel_data = [instance.get_image_nparray() for instance in self.instance_array]
        np_array = np.stack(pixel_data,axis=-1)
        return np_array


    def get_z_positions(self) -> list :
        """method to gather z positions of each dicom in serie

        Returns:
            [list]: [return list of z positions]
        """
        Z_positions = [ instance.get_image_position()[2] for instance in self.instance_array ]
        return Z_positions

    
    def get_z_spacing(self) -> float:
        """method to calculate z_spacing 

        Raises:
            Exception: [raise Exception if unconstant z spacing]]

        Returns:
            [float]: [return z spacing value]
        """
        Z_positions = [ instance.get_image_position()[2] for instance in self.instance_array ]
        #print(Z_positions)
        
        initial_z_spacing = round(abs(Z_positions[0] - Z_positions[1]), 1)
        for i in range(2,len(Z_positions)):

            z_spacing = round(abs(Z_positions[i - 1] - Z_positions[i]), 1)
            if z_spacing < initial_z_spacing - float(0.1) or z_spacing > initial_z_spacing + float(0.1) :
                try : 
                    raise Exception('Unconstant Spacing')
                except Exception : 
                    return('Unconstant Spacing') #alerte #return
        return np.mean(self.calculate_z_spacing(round_=False))
        


    def calculate_z_spacing(self, round_:bool = False) -> list : 
        """method to calculate the z_spacing between slice and gather in list

        Args:
            round_ (bool, optional): [choose if round the z_position or not]. Defaults to False.

        Returns:
            [list]: [return list of z spacing]
        """
        Z_positions = [ instance.get_image_position()[2] for instance in self.instance_array ]
        spacing = []
        if round_ == False : 
            initial_z_spacing = Z_positions[0] - Z_positions[1]
            spacing.append(initial_z_spacing)
            for i in range(2,len(Z_positions)):
                z_spacing = Z_positions[i - 1] - Z_positions[i]
                spacing.append(z_spacing)
            return spacing

        else : 
            initial_z_spacing = round(abs(Z_positions[0] - Z_positions[1]), 1)
            spacing.append(initial_z_spacing)
            for i in range(2,len(Z_positions)):
                z_spacing = round(abs(Z_positions[i - 1] - Z_positions[i]), 1)
                spacing.append(z_spacing)  
            return spacing 


    def get_all_SOPInstanceIUD(self)-> list:
        """method to gather all SOPInstanceUID of every Instance in serie

        Returns:
            [list]: [list of every SOPInstanceUID]
        """
        liste = []
        for instance in self.instance_array : 
            liste.append(instance.get_SOPInstanceUID())
        return liste 


    def get_all_acquisition_time(self) -> list :
        """method to gather all AcquisitionTime of every Instance in serie

        Returns:
            [list]: [list of every Acquisition Time]
        """
        liste = []
        for filename in self.file_names : 
            instanceData = Instance(os.path.join(self.path,filename), load_image=True)
            liste.append(instanceData.get_acquisition_time())
        return sorted(liste)


    def get_size_matrix(self) -> list :
        """method to get size of PET matrix/array 

        Returns:
            [list]: [  [x,y,z]  ]
        """
        size = []
        data = self.get_first_instance_metadata()
        x = data.get_number_rows()
        size.append(x)
        y = data.get_number_columns()
        size.append(y)
        z = len(self.get_all_SOPInstanceIUD())
        size.append(z)
        return size

    def export_nifti(self, file_path:str):
        """method to export ndarray of series to nifti and save it 

        Args:
            file_path (str): [directory+filename of the nifti]
        """
        sitk_img = sitk.GetImageFromArray( np.transpose(self.get_numpy_array(), (2,0,1) ))
        original_pixel_spacing = self.instance_array[0].get_pixel_spacing()          
        original_direction = self.instance_array[0].get_image_orientation()
        sitk_img.SetDirection( (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                    float(original_direction[3]), float(original_direction[4]), float(original_direction[5]), 
                                    0.0, 0.0, 1.0) )
        sitk_img.SetOrigin( self.instance_array[0].get_image_position() )
        sitk_img.SetSpacing( (original_pixel_spacing[0], original_pixel_spacing[1], self.get_z_spacing()) )
        sitk.WriteImage(sitk_img, file_path)

