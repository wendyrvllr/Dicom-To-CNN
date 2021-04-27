
from library_dicom.dicom_processor.model.Series import Series

from library_dicom.export_segmentation.rtstruct.StructureSetROISequence import StructureSetROISequence
from library_dicom.export_segmentation.rtstruct.RTROIObservationsSequence import RTROIObservationsSequence
from library_dicom.export_segmentation.rtstruct.ROIContourSequence import ROIContourSequence
from library_dicom.export_segmentation.rtstruct.ReferencedFrameOfReferenceSequence import ReferencedFrameOfReferenceSequence
from library_dicom.export_segmentation.tools.generate_dict import *
from library_dicom.export_segmentation.tools.rtss_writer_tools import *
import pydicom
import datetime
import random 
import warnings
import os 
import numpy as np 
import tempfile 

#DOCU : 
# MASK : NDARRAY 3D [Z, X, Y] BINARY OR SITK IMG (X, Y, Z) => CHAQUE SLICE NE DOIT PAS AVOIR MOINS DE 3 PIXELS ISOLES
#(cf clean in init)
#DICT : generate_dict in tools : PAS PLUS DE 16 CARACTERES 
class RTSS_Writer:
    """A class for DICOM RT format
    """
    
    def __init__(self, mask, serie_path, mask_mode):
        """[summary]

        Args:
            mask ([ndarray or sitk_img]): []
            serie_path ([str]): [Serie path related to RTSTRUCT file ]
            mask_mode ([str]) : ['img' if a sitk_img or 'matrix' if ndarray]
        """

        self.mask = mask
        self.mask_mode = mask_mode 

        serie = Series(serie_path)
        self.instances = serie.get_instances_ordered()


        if mask_mode == 'matrix' : 
            self.mask_array = mask # 3D ndarray [z, x, y]
            self.mask_img = sitk.GetImageFromArray(self.mask_array)
            #data spécifique à la série ou on dessine les contours : origin, spacing, direction 

            self.image_position = self.instances[0].get_image_position() #origin 
            self.pixel_spacing = self.instances[0].get_pixel_spacing()
            self.pixel_spacing.append(abs(serie.get_z_spacing())) #spacing 
            original_direction = self.instances[0].get_image_orientation()
            self.image_direction = (float(original_direction[0]), float(original_direction[1]), float(original_direction[2]), 
                                        float(original_direction[3]), float(original_direction[4]), abs(float(original_direction[5])), 
                                        0.0, 0.0, 1.0) 
            self.mask_img.SetSpacing(self.pixel_spacing)
            self.mask_img.SetOrigin(self.image_position)
            self.mask_img.SetDirection(self.image_direction)

        elif mask_mode == 'img' : 
            self.mask_img = mask
            self.mask_array = read_sitk_img(self.mask_img) # 3Dndarray [z,x,y]
            self.image_position = self.mask_img.GetOrigin()
            self.pixel_spacing = self.mask_img.GetSpacing()
            self.image_direction = self.mask_img.GetDirection()

        #get number of ROI after label
        self.number_of_roi = int(np.max(self.mask_array))



        #Get list of every sop instance uid 
        self.list_all_SOPInstanceUID = get_list_SOPInstance_UID(self.instances)

        #generate dictionnary with paramter inside 
        self.generate_dict_json()

        #creation file_meta 
        self.file_meta, self.file_meta.MediaStorageSOPInstanceUID = self.generates_file_meta()
        suffix = '.dcm'
        filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
        self.dataset = pydicom.dataset.FileDataset(filename_little_endian, {}, file_meta=self.file_meta, preamble=b"\0" * 128)

        #Add the data element in FileDataset
        self.set_tags()
        self.set_StructureSetROISequence()
        self.set_RTROIObservationSequence()
        self.set_ROIContourSequence()
        self.set_ReferencedFrameOfReferenceSequence()
        
        # Set the transfer syntax
        self.dataset.is_little_endian = True
        self.dataset.is_implicit_VR = False 

    def generate_dict_json(self):
        number_of_roi = get_number_of_roi(self.mask_array)
        results = generate_dict(number_of_roi, 'rtstruct')
        self.results = results
        return None 

    def generates_file_meta(self):
        """
            Generates required values for file meta information
            List of tags :
                  - FileMetaInformationGroupLength':
                  - FileMetaInformationVersion'    :
                  - MediaStorageSOPClassUID'       :
                  - MediaStorageSOPInstanceUID'    :
                  - TransferSyntaxUID'             :
                  - ImplementationClassUID'        :
        """


        file_meta = pydicom.dataset.FileMetaDataset()

        file_meta.FileMetaInformationGroupLength = 166
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3' # RT Structure Set Storage
        file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        #self.dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID 
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian #pydicom.uid.ImplicitVRLittleEndian #pydicom.uid.ExplicitVRLittleEndian  #Implicit VR Little Endian
        file_meta.ImplementationClassUID =  pydicom.uid.PYDICOM_IMPLEMENTATION_UID #'1.2.246.352.70.2.1.7'
        
        return file_meta, file_meta.MediaStorageSOPInstanceUID


    def set_tags(self):
        """
            
            List of tags :
                  - AccessionNumber'       :
                  - PatientBirthDate'      :
                  - PatientBirthTime'      :
                  - PatientID'             :
                  - PatientName'           :
                  - PatientSex'            :
                  - PhysiciansOfRecord'    :
                  - ReferringPhysicianName':
                  - SpecificCharacterSet'  :
                  - StudyDate'             :
                  - StudyDescription'      :
                  - StudyID'               :
                  - StudyInstanceUID'      :
                  - StudyTime'             : 
        """     
        #from the serie 
        self.dataset.AccessionNumber = self.instances[0].get_accession_number()
        self.dataset.PatientBirthDate = self.instances[0].get_patient_birth_date()
        self.dataset.PatientID = self.instances[0].get_patient_id()
        self.dataset.PatientName = self.instances[0].get_patient_name()
        self.dataset.PatientSex = self.instances[0].get_patient_sex()
        self.dataset.PhysiciansOfRecord = self.instances[0].get_physicians_of_record()
        self.dataset.ReferringPhysicianName = self.instances[0].get_referring_physician_name()
        self.dataset.SpecificCharacterSet = self.instances[0].get_specific_character_set()
        self.dataset.StudyDate = self.instances[0].get_study_date()
        self.dataset.StudyDescription = self.instances[0].get_study_description()
        self.dataset.StudyID = self.instances[0].get_study_id()
        self.dataset.StudyInstanceUID = self.instances[0].get_study_instance_uid()
        self.dataset.StudyTime = self.instances[0].get_study_time()

        #specific new tags for the serie 
        self.dataset.ApprovalStatus = 'UNAPPROVED'
        self.dataset.Manufacturer   = ''
        dt = datetime.datetime.now()
        self.dataset.InstanceCreationDate = dt.strftime('%Y%m%d')
        self.dataset.InstanceCreationTime = dt.strftime('%H%M%S.%f')
        self.dataset.InstanceNumber = '1'
        self.dataset.Modality = 'RTSTRUCT'
        self.dataset.ReviewDate = '' #because UNAPPROVED
        self.dataset.ReviewTime = '' #because UNAPPROVED
        self.dataset.ReviewerName = '' #because UNAPPROVED
        self.dataset.SeriesDescription = self.results["SeriesDescription"]
        self.dataset.SeriesInstanceUID = pydicom.uid.generate_uid()
        self.dataset.SeriesNumber = random.randint(0,1e3)
        self.dataset.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3' 
        self.dataset.SOPInstanceUID = self.file_meta.MediaStorageSOPInstanceUID
        self.dataset.StructureSetDate = dt.strftime('%Y%m%d')
        self.dataset.StructureSetDescription = self.results["SeriesDescription"]
        self.dataset.StructureSetLabel = self.results["SeriesDescription"]
        self.dataset.StructureSetTime = dt.strftime('%H%M%S.%f')

        return None 



    #StructureSetROISequence
    def set_StructureSetROISequence(self):
        referenced_frame_of_reference_uid = self.instances[0].get_frame_of_reference_uid()
        self.dataset.StructureSetROISequence = StructureSetROISequence(self.mask_array, self.results, self.number_of_roi).create_StructureSetROISequence(self.pixel_spacing, referenced_frame_of_reference_uid)
        

    #RTROIObservationSequence
    def set_RTROIObservationSequence(self):
        self.dataset.RTROIObservationsSequence = RTROIObservationsSequence(self.results, self.number_of_roi).create_RTROIObservationsSequence()
        

    #ROIContourSequence 
    def set_ROIContourSequence(self):
        referenced_sop_class_uid = self.instances[0].get_sop_class_uid()
        self.dataset.ROIContourSequence = ROIContourSequence(self.mask_array, self.mask_img, self.number_of_roi).create_ROIContourSequence(referenced_sop_class_uid, self.list_all_SOPInstanceUID, self.instances)

    #ReferencedFrameOfReferenceSequence 
    def set_ReferencedFrameOfReferenceSequence(self):
        frame_of_reference_uid = self.instances[0].get_frame_of_reference_uid()
        series_instance_uid = self.instances[0].get_series_instance_uid()
        study_instance_uid = self.instances[0].get_study_instance_uid()
        sop_class_uid = self.instances[0].get_sop_class_uid()
        self.dataset.ReferencedFrameOfReferenceSequence = ReferencedFrameOfReferenceSequence().create_ReferencedFrameOfReferenceSequence(frame_of_reference_uid, sop_class_uid, self.list_all_SOPInstanceUID, series_instance_uid, study_instance_uid)


    def save_file(self, filename, directory_path):
        #filemeta = self.generates_file_meta()
        #filedataset = pydicom.dataset.FileDataset(filename, self.dataset, preamble=b"\0" * 128, file_meta=filemeta, is_implicit_VR = True, is_little_endian = True )
        #filedataset.save_as(os.path.join(directory_path, filename))
        self.dataset.save_as(os.path.join(directory_path, filename), write_like_original=False)
        return None 


        
        

    
