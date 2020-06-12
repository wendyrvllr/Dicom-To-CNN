from library_dicom.rtss_processor.model.ROI_RTSS import ROI_RTSS
from library_dicom.dicom_processor.model.Series import Series
import pydicom
import datetime
import random 
import warnings
import os 


class RTSS_Writer():
    """A class for DICOM RT format
    """
    
    def __init__(self, mask, serie_path):
        self.mask = mask

        self.file_meta = self.generates_file_meta()

        #Generates FileDataset element
        #super().__init__(filename,{},file_meta=self.file_meta, preamble=b"\0" * 128)

        # FileDataset specific fields
        self.is_little_endian = True
        self.is_implicit_VR = True

        self.set_tags(serie_path)
        self.set_RTSTRUCT_tags()


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
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2' #Implicit VR Little Endian
        file_meta.ImplementationClassUID = '1.2.246.352.70.2.1.7'
        
        return file_meta


    def GatherTags(self, serie_path): #a partir d'une CT ou PT récuperer les infos 
        serie = Series(serie_path)
        Tags = {'AccessionNumber':None,
                #'DeviceSerialNumber':None,
                #'Manufacturer':None,
                #'ManufacturerModelName':None,
                'PatientBirthDate':None,
                'PatientBirthTime':None,
                'PatientID':None,
                'PatientName':None,
                'PatientSex':None,
                'PhysiciansOfRecord':None,
                'ReferringPhysicianName':None,
                #'SoftwareVersions':None,
                'SeriesInstanceUID':None,
                'SpecificCharacterSet':None,
                #'StationName':None,
                'StudyDate':None,
                'StudyDescription':None,
                'StudyID':None,
                'StudyInstanceUID':None,
                'StudyTime':None,
                'FrameOfReferenceUID':None,
                'SOPClassUID':None
                }
        
        with pydicom.dcmread(os.path.join(serie_path, serie.file_names[0])) as dcm:

            for tag in Tags.keys():
                try:
                    Tags[tag] = dcm.get(tag)
                except AttributeError:
                    warnings.warn("AttributeError with tag: %s" % tag)
                    pass
                except Exception:
                    raise Exception


        
        return Tags

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
        #dataset = pydicom.dataset.Dataset()
        tags = self.GatherTags(serie_path)

        self.AccessionNumber = tags['AccessionNumber']
        #dataset.AccessionNumber = tags['AccessionNumber']
        self.PatientBirthDate = tags['PatientBirthDate']
        self.PatientBirthTime = tags['PatientBirthTime']
        self.PatientID = tags['PatientID']
        self.PatientName = tags['PatientName']
        self.PatientSex = tags['PatientSex']
        self.PhysiciansOfRecord = tags['PhysiciansOfRecord']
        self.ReferringPhysicianName = tags['ReferringPhysicianName']
        self.SpecificCharacterSet = tags['SpecificCharacterSet']
        self.StudyDate = tags['StudyDate']
        self.StudyDescription = tags['StudyDescription']
        self.StudyID = tags['StudyID']
        self.StudyInstanceUID = tags['StudyInstanceUID']
        self.StudyTime = tags['StudyTime']
        
    
        return None 


    def set_RTSTRUCT_tags(self):
        """
            Generates new values for tags specific to RTSTRUCT file
            List custom tags:
                  - AccessionNumber'       :
                  - PatientBirthDate'      :
                  - PatientBirthTime'      :
                  - PatientID'             :
                  - PatientName'           :
                  - PatientSex'            :
            List randomly generated tags:
                  - AccessionNumber'       :
                  - PatientBirthDate'      :
                  - PatientBirthTime'      :
                  - PatientID'             :
                  - PatientName'           :
                  - PatientSex'            :
            
        """
        #dataset = pydicom.dataset.Dataset()

        self.ApprovalStatus = 'UNAPPROVED'
        self.Manufacturer   = ''
        dt = datetime.datetime.now()
        self.InstanceCreationDate = dt.strftime('%Y%m%d')
        self.InstanceCreationTime = dt.strftime('%H%M%S.%f')
        self.InstanceNumber = '1'
        self.Modality = 'RTSTRUCT'
        self.ReviewDate = '' #because UNAPPROVED
        self.ReviewTime = '' #because UNAPPROVED
        self.ReviewerName = '' #because UNAPPROVED
        self.SeriesDescription = 'RTSTRUCT generated by library-DICOM'
        self.SeriesInstanceUID = pydicom.uid.generate_uid()
        self.SeriesNumber = random.randint(0,1e3)
        self.SOPClassUID = self.file_meta.MediaStorageSOPClassUID 
        self.SOPInstanceUID = self.file_meta.MediaStorageSOPInstanceUID 
        self.StructureSetDate = dt.strftime('%Y%m%d')
        self.StructureSetDescription = 'RTSTRUCT generated by library-DICOM'
        self.StructureSetLabel = 'test'
        self.StructureSetTime = dt.strftime('%H%M%S.%f')
        
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


    def save_(self, filename):
        filedataset = pydicom.dataset.FileDataset()
        #put dataset in filedataset
        #save filedataset 

        
        

    
