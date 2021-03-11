
from library_dicom.dicom_processor.model.Series import Series

from library_dicom.rtss_processor.model.StructureSetROISequence import StructureSetROISequence
from library_dicom.rtss_processor.model.RTROIObservationsSequence import RTROIObservationsSequence
from library_dicom.rtss_processor.model.ROIContourSequence import ROIContourSequence
from library_dicom.rtss_processor.model.ReferencedFrameOfReferenceSequence import ReferencedFrameOfReferenceSequence

import pydicom
import datetime
import random 
import warnings
import os 



class RTSS_Writer:
    """A class for DICOM RT format
    """
    
    def __init__(self, mask, serie_path, dict_roi_data):
        self.mask = mask

        #data spécifique à la série ou on dessine les contours 
        serie = Series(serie_path)
        self.instances = serie.get_instances_ordered()
        self.image_position = self.instances[0].get_image_position()
        self.pixel_spacing = self.instances[0].get_pixel_spacing()
        self.pixel_spacing.append(serie.get_z_spacing())
        
        #Get list of every sop instance uid 
        self.list_all_SOPInstanceUID = serie.get_all_SOPInstanceIUD()
    
        #self.first_metadata = serie.get_first_instance_metadata()

        #str to float 
        for i in range(len(self.image_position)):
            self.image_position[i] = float(self.image_position[i])
            self.pixel_spacing[i] = float(self.pixel_spacing[i])


        #dictionnaire entrée par l'utilisateur 
        self.dict_roi_data = dict_roi_data

        #creation dataset 
        self.dataset = pydicom.dataset.Dataset()
        self.set_tags(serie_path)
        self.set_StructureSetROISequence()
        self.set_RTROIObservationSequence()
        self.set_ROIContourSequence()
        self.set_ReferencedFrameOfReferenceSequence()


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


        file_meta = pydicom.dataset.Dataset()

        file_meta.FileMetaInformationGroupLength = 166
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3' # RT Structure Set Storage
        file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        self.dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID 

        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2' #Implicit VR Little Endian
        file_meta.ImplementationClassUID = '1.2.246.352.70.2.1.7'
        
        return file_meta


    def set_tags(self,serie_path):
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
        self.dataset.PatientBirthData = self.instances[0].get_patient_birth_date()
        self.dataset.PatientID = self.instances[0].get_patient_id()
        self.dataset.PatientName = self.instances[0].get_patient_name()
        self.dataset.PatientSex = self.instances[0].get_patient_sex()
        self.dataset.PysiciansOfRecord = self.instances[0].get_physicians_of_record()
        self.dataset.ReferringPhysicianName = self.instances[0].get_referring_physician_name()
        self.dataset.SpecificCharacterSet = self.instances[0].get_specific_character_set()
        self.dataset.StudyData = self.instances[0].get_study_date()
        self.dataset.StudyDescription = self.instances[0].get_study_description()
        self.dataset.StudyID = self.instances[0].get_study_id()
        self.dataset.StudyInstanceUID = pydicom.uid.generate_uid() #self.instances[0].get_study_instance_uid()
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
        self.dataset.SeriesDescription = self.dict_roi_data['Description']
        self.dataset.SeriesInstanceUID = pydicom.uid.generate_uid()
        self.dataset.SeriesNumber = random.randint(0,1e3)
        self.dataset.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3' 
        #self.dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID 
        self.dataset.StructureSetDate = dt.strftime('%Y%m%d')
        self.dataset.StructureSetDescription = self.dict_roi_data['Description']
        self.dataset.StructureSetLabel = self.dict_roi_data['Description']
        self.dataset.StructureSetTime = dt.strftime('%H%M%S.%f')

        return None 



    #StructureSetROISequence
    def set_StructureSetROISequence(self):
        referenced_frame_of_reference_uid = self.instances[0].get_frame_of_reference_uid()
        self.dataset.StructureSetROISequence = StructureSetROISequence(self.mask, self.dict_roi_data).create_StructureSetROISequence(self.pixel_spacing, referenced_frame_of_reference_uid)
        

    #RTROIObservationSequence
    def set_RTROIObservationSequence(self):
        self.dataset.RTROIObservationsSequence = RTROIObservationsSequence(self.mask, self.dict_roi_data).create_RTROIObservationsSequence()
        

    #ROIContourSequence 
    def set_ROIContourSequence(self):
        referenced_sop_class_uid = self.instances[0].get_sop_class_uid()
        self.dataset.ROIContourSequence = ROIContourSequence(self.mask, self.dict_roi_data).create_ROIContourSequence(referenced_sop_class_uid, self.image_position, self.pixel_spacing, self.list_all_SOPInstanceUID, self.instances)

    #ReferencedFrameOfReferenceSequence 
    def set_ReferencedFrameOfReferenceSequence(self):
        frame_of_reference_uid = self.instances[0].get_frame_of_reference_uid()
        series_instance_uid = self.instances[0].get_series_instance_uid()
        study_instance_uid = self.instances[0].get_study_instance_uid()
        sop_class_uid = self.instances[0].get_sop_class_uid()
        self.dataset.ReferencedFrameOfReferenceSequence = ReferencedFrameOfReferenceSequence().create_ReferencedFrameOfReferenceSequence(frame_of_reference_uid, sop_class_uid, self.list_all_SOPInstanceUID, series_instance_uid, study_instance_uid)


    def save_file(self, filename, directory_path):
        filemeta = self.generates_file_meta()
        filedataset = pydicom.dataset.FileDataset(filename, self.dataset, preamble=b"\0" * 128, file_meta=filemeta, is_implicit_VR = True, is_little_endian = True )
        filedataset.save_as(os.path.join(directory_path, filename))

        return None 


        
        

    
