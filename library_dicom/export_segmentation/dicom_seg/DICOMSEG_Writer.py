import pydicom_seg 
import pydicom 
import numpy as np 
import json 
import os
from library_dicom.export_segmentation.tools.generate_dict import *
import SimpleITK as sitk 


class DICOMSEG_Writer:

    def __init__(self, img_mask, serie_path):
        """[summary]

        Args:
            img_mask ([sitk Image]): [sitk image of mask]
            serie_path ([str]): [Path to an imaging serie related to the segmentation ]
        """

        self.img_mask = img_mask
        self.serie_path = serie_path

    def generate_dict_json(self, directory_path):
        pred_array = sitk.GetArrayFromImage(self.img_mask)
        number_of_roi = np.max(pred_array)
        results = generate_dict(number_of_roi)
        self.results = results
        json_path = save_dict_as_json(results, directory_path)
        return json_path 



    def dicom_seg_writer(self, directory_path):
        json_path = self.generate_dict_json(directory_path)

        segmentation = self.img_mask
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


    def save_file(self, filename, directory_path):
        dcm = self.dicom_seg_writer(directory_path)
        dcm.save_as(os.path.join(directory_path, filename))
        return None 