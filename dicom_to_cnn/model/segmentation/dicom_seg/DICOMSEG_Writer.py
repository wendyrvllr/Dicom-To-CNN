import pydicom_seg 
import pydicom 
import numpy as np 
import os
from dicom_to_cnn.tools.export_segmentation.generate_dict import *
from dicom_to_cnn.model.segmentation.Abstract_Writer import Abstract_Writer
import SimpleITK as sitk 


class DICOMSEG_Writer(Abstract_Writer):
    """a class to write a DICOMSEG file
    """

    def __init__(self, mask_img:sitk.Image, serie_path:str):
        """constructor

        Args:
            img_mask ([sitk.Image]): [sitk img of segmentation, [x,y,z]]
            serie_path ([str]): [Serie path related to DICOMSEG file]
        """
        super().__init__(mask_img)
        self.serie_path = serie_path

    def __generate_dict_json(self, directory_path:str) -> str:
        """method to generate dict with metainfo for DICOM SEG file and save it as json file

        Args:
            directory_path (str): [directory's path where to save the json file with metainfo]

        Returns:
            [str]: [return the path of the json generated]
        """
        pred_array = sitk.GetArrayFromImage(self.mask_img)
        number_of_roi = np.max(pred_array)
        results = generate_dict(number_of_roi, 'dicomseg')
        self.results = results
        json_path = save_dict_as_json(results, directory_path)
        return json_path 

    def dicom_seg_writer(self, directory_path:str) -> pydicom.FileDataset:
        """method to write a DICOMSEG file from a segmentation

        Args:
            directory_path (str): [directory's path where to save the json file with metainfo]

        Returns:
            [pydicom.FileDataset]: [return the new DICOMSEG]
        """
        json_path = self.__generate_dict_json(directory_path)

        segmentation = self.mask_img
        dicom_file = os.listdir(self.serie_path)
        dicom_series_paths = [os.path.join(self.serie_path, x) for x in dicom_file]
        source_images = [
            pydicom.dcmread(x, stop_before_pixels=True)
            for x in dicom_series_paths]

        template = pydicom_seg.template.from_dcmqi_metainfo(json_path)

        writer = pydicom_seg.MultiClassWriter(
                template=template,
                inplane_cropping=False,  # Crop image slices to the minimum bounding box on
                                        # x and y axes. Maybe not supported by other frameworks.
                skip_empty_slices=True,  # Don't encode slices with only zeros
                skip_missing_segment=False,  # If a segment definition is missing in the
                                            # template, then raise an error instead of
                                            # skipping it.
            )

        dcm = writer.write(segmentation, source_images)
        return dcm


    def save_file(self, filename:str, directory_path:str) -> None :
        """method to save the new DICOMSEG file

        Args:
            filename (str): [name of the new DICOMSEG file]
            directory_path (str): [directory's path where to save the new DICOMSEG file]

        """
        dcm = self.dicom_seg_writer(directory_path)
        dcm.save_as(os.path.join(directory_path, filename))