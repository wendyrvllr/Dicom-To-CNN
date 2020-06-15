from library_dicom.rtss_processor.model.ROI_RTSS import ROI_RTSS
from library_dicom.dicom_processor.model.Series import Series
from library_dicom.rtss_processor.model.Mask_To_RTSS import Mask_To_RTSS
import pydicom
import datetime
import random 
import warnings
import os 



class RTSS_Writer:
    """A class for DICOM RT format
    """
    #Instancer objet Serie pour pixel spacing etc 
    def __init__(self, mask, serie_path):
        self.mask = mask

        #spécifique pour calculer les contours des ROIS
        serie = Series(serie_path)
        self.first_metadata = serie.get_first_instance_metadata()
        self.image_position = self.first_metadata.get_image_position()
        self.pixel_spacing = self.first_metadata.get_pixel_spacing()
        serie.get_numpy_array()
        self.pixel_spacing.append(serie.get_z_spacing())
        self.list_all_SOPInstanceUID = serie.get_all_SOPInstanceIUD()

        #creation dataset 

        self.dataset  = pydicom.dataset.Dataset()
        self.set_tags(serie_path)


        #self.file_meta = self.generates_file_meta()

        #Generates FileDataset element
        #super().__init__(filename,{},file_meta=self.file_meta, preamble=b"\0" * 128)



        #self.set_tags(serie_path)
        #self.set_RTSTRUCT_tags()


        self.RTROIObservationsSequence = pydicom.sequence.Sequence()
        self.ROIContourSequence = pydicom.sequence.Sequence()
        self.StructureSetROISequence = pydicom.sequence.Sequence()
        self.ReferencedFrameOfReferenceSequence = pydicom.sequence.Sequence()



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
        self.dataset.AccessionNumber = self.first_metadata.get_accession_number()
        self.dataset.PatientBirthData = self.first_metadata.get_patient_birth_date()
        self.dataset.PatientID = self.first_metadata.get_patient_id()
        self.dataset.PatientName = self.first_metadata.get_patient_name()
        self.dataset.PatientSex = self.first_metadata.get_patient_sex()
        #self.dataset.PysiciansOfRecord = self.first_metadata.get_physicians_of_record()
        self.dataset.ReferringPhysicianName = self.first_metadata.get_referring_physician_name()
        self.dataset.SpecificCharacterSet = self.first_metadata.get_specific_character_set()
        self.dataset.StudyData = self.first_metadata.get_study_date()
        self.dataset.StudyDescription = self.first_metadata.get_study_description()
        self.dataset.StudyID = self.first_metadata.get_study_id()
        self.dataset.StudyInstanceUID = self.first_metadata.get_study_instance_uid()
        self.dataset.StudyTime = self.first_metadata.get_study_time()

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
        self.dataset.SeriesDescription = 'RTSTRUCT generated by library-DICOM'
        self.dataset.SeriesInstanceUID = pydicom.uid.generate_uid()
        self.dataset.SeriesNumber = random.randint(0,1e3)
        self.dataset.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3' 
        #self.dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID 
        self.dataset.StructureSetDate = dt.strftime('%Y%m%d')
        self.dataset.StructureSetDescription = 'RTSTRUCT generated by library-DICOM'
        self.dataset.StructureSetLabel = 'test'
        self.dataset.StructureSetTime = dt.strftime('%H%M%S.%f')

        return None 



    #StructureSetROISequence
    def set_StructureSetROISequence(self, ROINumber, ReferencedFrameOfReferenceUID, ROIName, ROIDescription, ROIVolume, ROIGenerationAlgorithm):
        self.StructureSetROI = pydicom.dataset.Dataset()
        self.StructureSetROI.ROINumber = ROINumber
        self.StructureSetROI.ReferencedFrameOfReferenceUID = str(ReferencedFrameOfReferenceUID)
        self.StructureSetROI.ROIName = ROIName
        self.StructureSetROI.ROIDescription = ROIDescription
        self.StructureSetROI.ROIVolume = ROIVolume
        self.StructureSetROI.ROIGenerationAlgorithm = ROIGenerationAlgorithm
        self.StructureSetROISequence.append(self.StructureSetROI)


    def get_StructureSetROISequence(self):
        return self.StructureSetROISequence

    

    #RTROIObservationSequence
    def set_RTROIObservationSequence(self, ObservationNumber, ReferencedROINumber, ROIObservationLabel, RTROIInterpretedType):
        self.RTROIObservation = pydicom.dataset.Dataset()
        
        self.RTROIObservation.ObservationNumber = ObservationNumber
        self.RTROIObservation.ReferencedROINumber = ReferencedROINumber
        self.RTROIObservation.ROIObservationLabel = ROIObservationLabel
        self.RTROIObservation.RTROIInterpretedType = RTROIInterpretedType
        self.RTROIObservationsSequence.append(self.RTROIObservation)
        #return self.RTROIObservationSequence
        

    def get_RTROIObservationSequence(self):
        return self.RTROIObservationsSequence


    #ReferencedFrameOfReferencSequence 
    def set_ContourImageSequence(self, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        self.ContourImage = pydicom.sequence.Sequence()
        for SOPInstanceUID in list_all_SOPInstanceUID : 
            dataset= pydicom.dataset.Dataset()
            dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
            dataset.ReferencedSOPInstanceUID = SOPInstanceUID
            self.ContourImage.append(dataset)
        #print(type(self.ContourImageSequence))
        return self.ContourImage 


    def set_RTReferencedSeriesSequence(self, SeriesInstanceUID,ReferencedSOPClassUID, list_all_SOPInstanceUID):
        #self.RTReferencedSeriesSequence = pydicom.sequence.Sequence()
        self.RTReferencedSeries = pydicom.dataset.Dataset()
        self.RTReferencedSeries.SeriesInstanceUID = SeriesInstanceUID
        self.RTReferencedSeries.ContourImageSequence = self.set_ContourImageSequence(ReferencedSOPClassUID, list_all_SOPInstanceUID)
        #print(type(self.RTReferencedSeries))
        return self.RTReferencedSeries

    def set_RTReferencedStudySequence(self, ReferencedSOPInstanceUID, SeriesInstanceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        self.RTReferencedStudy = pydicom.dataset.Dataset()
        self.RTReferencedStudy.ReferencedSOPInstanceUID = ReferencedSOPInstanceUID
        self.RTReferencedStudy.RTReferencedSeriesSequence = pydicom.sequence.Sequence()
        self.RTReferencedStudy.RTReferencedSeriesSequence.append(self.set_RTReferencedSeriesSequence(SeriesInstanceUID,ReferencedSOPClassUID, list_all_SOPInstanceUID))
        #print(type(self.RTReferencedStudy))
        return self.RTReferencedStudy

    def set_ReferencedFrameOfReferenceSequence(self, FrameOfReferenceUID, ReferencedSOPInstanceUID, SeriesInstanceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        self.ReferencedFrameOfReference = pydicom.dataset.Dataset()
        self.ReferencedFrameOfReference.FrameOfReferenceUID = FrameOfReferenceUID
        self.ReferencedFrameOfReference.RTReferencedStudySequence = pydicom.sequence.Sequence()
        self.ReferencedFrameOfReference.RTReferencedStudySequence.append(self.set_RTReferencedStudySequence(ReferencedSOPInstanceUID, SeriesInstanceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID))
        #print(type(self.ReferencedFrameOfReference))
        self.ReferencedFrameOfReferenceSequence.append(self.ReferencedFrameOfReference)

    def get_ReferencedFrameOfReferenceSequence(self):
        return self.ReferencedFrameOfReferenceSequence


    #ContourROISequence

    def set_ROIContourSequence(self, ReferencedROINumber, DisplayColor, ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData):
        self.ROIContour = pydicom.dataset.Dataset()
        roi_rtss = ROI_RTSS()
        roi_contour_sequence = roi_rtss.set_ROIContour(ReferencedROINumber, DisplayColor, ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData)
        #self.ROIContour.ContourSequence = roi_contour_sequence 
        #print(self.ROIContour)
        #self.ROIContourSequence.append(self.ROIContour)
        self.ROIContourSequence.append(roi_contour_sequence)

    def get_ROIContourSequence(self):
        return self.ROIContourSequence 


    def save_(self, filename, directory_path):
        filemeta = self.generates_file_meta()

        filedataset = pydicom.dataset.FileDataset(filename, self.dataset #dataset ici 
        , preamble=b"\0" * 128, file_meta=filemeta, is_implicit_VR = True, is_little_endian = True )
        #filedataset.PatientName = ...
        #filedataset.... = ... 
        #filedataset.append(self.data)
        filedataset.save_as(os.path.join(directory_path, filename))

        return None 
        #put dataset in filedataset
        #save filedataset 

        
        

    
