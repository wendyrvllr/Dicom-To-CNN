from library_dicom.rtss_processor.model.ROI_RTSS import ROI_RTSS
from library_dicom.dicom_processor.model.Series import Series
import pydicom
import datetime
import random 
import warnings
import os 

from library_dicom.new_RTSTRUCT.RTROIObservations import RTROIObservations
from library_dicom.new_RTSTRUCT.ROIContour import ROIContour
from library_dicom.new_RTSTRUCT.StructureSetROI import StructureSetROI
from library_dicom.new_RTSTRUCT.ReferencedFrameOfReference import ReferencedFrameOfReference



class RTSS(pydicom.dataset.FileDataset):
    """A class for DICOM RT format
    """
    
    def __init__(self, origin, filename, serie_path):
        self.origin = origin

        self.file_meta = self.generates_file_meta()

        #Generates FileDataset element
        super().__init__(filename,{},file_meta=self.file_meta, preamble=b"\0" * 128)

        # FileDataset specific fields
        self.is_little_endian = True
        self.is_implicit_VR = True

        self.tags = self.generates_tags(serie_path)
        self.RTSS_tags = self.generates_RTSTRUCT_tags()

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

    def get_SOPInstanceUID(self, serie_path): #pour le set ReferencedFrameOfReferenceSequence
        serie = Series(serie_path)
        list_SOPInstanceUID = serie.get_all_SOPInstanceIUD()
        return list_SOPInstanceUID


    def __GatherTags(self, serie_path): #a partir d'une CT ou PT récuperer les infos 
        serie = Series(serie_path)
        #first_dicom_path = os.path.join(serie_path, serie.file_names[0])
        #print(first_dicom_path)
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

        # force write list_SOPInstanceUID to Tags (must not be directly herited!)
        #Tags['list_SOPInstanceUID'] = self.__get_SOPInstanceUID(serie_path)
        
        return Tags

    def generates_tags(self,serie_path):
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
        file_meta = pydicom.dataset.Dataset()
        tags = self.__GatherTags(serie_path)


        file_meta.AccessionNumber = tags['AccessionNumber']
        file_meta.PatientBirthDate = tags['PatientBirthDate']
        file_meta.PatientBirthTime = tags['PatientBirthTime']
        file_meta.PatientID = tags['PatientID']
        file_meta.PatientName = tags['PatientName']
        file_meta.PatientSex = tags['PatientSex']
        file_meta.PhysiciansOfRecord = tags['PhysiciansOfRecord']
        file_meta.ReferringPhysicianName = tags['ReferringPhysicianName']
        file_meta.SpecificCharacterSet = tags['SpecificCharacterSet']
        file_meta.StudyDate = tags['StudyDate']
        file_meta.StudyDescription = tags['StudyDescription']
        file_meta.StudyID = tags['StudyID']
        file_meta.StudyInstanceUID = tags['StudyInstanceUID']
        file_meta.StudyTime = tags['StudyTime']
        #file_meta.list_SOPInstanceUID = tags['list_SOPInstanceUID']
    
        return file_meta


    def generates_RTSTRUCT_tags(self):
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
        file_meta = pydicom.dataset.Dataset()

        file_meta.ApprovalStatus = 'UNAPPROVED'
        file_meta.Manufacturer   = ''
        dt = datetime.datetime.now()
        file_meta.InstanceCreationDate = dt.strftime('%Y%m%d')
        file_meta.InstanceCreationTime = dt.strftime('%H%M%S.%f')
        file_meta.InstanceNumber = '1'
        file_meta.Modality = 'RTSTRUCT'
        file_meta.ReviewDate = '' #because UNAPPROVED
        file_meta.ReviewTime = '' #because UNAPPROVED
        file_meta.ReviewerName = '' #because UNAPPROVED
        file_meta.SeriesDescription = 'RTSTRUCT generated by library-DICOM'
        file_meta.SeriesInstanceUID = pydicom.uid.generate_uid()
        file_meta.SeriesNumber = random.randint(0,1e3)
        file_meta.SOPClassUID = self.file_meta.MediaStorageSOPClassUID 
        file_meta.SOPInstanceUID = self.file_meta.MediaStorageSOPInstanceUID 
        file_meta.StructureSetDate = dt.strftime('%Y%m%d')
        file_meta.StructureSetDescription = 'RTSTRUCT generated by library-DICOM'
        file_meta.StructureSetLabel = 'test'
        file_meta.StructureSetTime = dt.strftime('%H%M%S.%f')
        
        return file_meta 

    #StructureSetROISequence
    def set_StructureSetROISequence(self, ROINumber, ReferencedFrameOfReferenceUID, ROIName, ROIDescription, ROIVolume, ROIGenerationAlgorithm):
        self.StructureSetROI = pydicom.dataset.Dataset()
        self.StructureSetROI.ROINumber = ROINumber
        self.StructureSetROI.ReferencedFrameOfReferenceUID = str(ReferencedFrameOfReference)
        self.StructureSetROI.ROIName = ROIName
        self.StructureSetROI.ROIDescription = ROIDescription
        self.StructureSetROI.ROIVolume = ROIVolume
        self.StructureSetROI.ROIGenerationAlgorithm = ROIGenerationAlgorithm
        self.StructureSetROISequence.append(self.StructureSetROI)


    def get_StructureSetROISequence(self):
        return self.StructureSetROISequence

    

    #RTROIObservationSequence
    def set_RTROIObservationSequence(self, ObservationNumber, ReferencedROINumber):
        self.RTROIObservation = pydicom.dataset.Dataset()
        self.RTROIObservation.ObservationNumber = ObservationNumber
        self.RTROIObservation.ReferencedROINumber = ReferencedROINumber
        self.RTROIObservationsSequence.append(self.RTROIObservation)
        

    def get_RTROIObservationSequence(self):
        return self.RTROIObservationsSequence


    #ReferencedFrameOfReferencSequence 
    def set_ContourImageSequence(self, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        self.ContourImageSequence = pydicom.sequence.Sequence()
        for SOPInstanceUID in list_all_SOPInstanceUID : 
            contourImage = pydicom.dataset.Dataset()
            contourImage.ReferencedSOPClassUID = ReferencedSOPClassUID
            contourImage.ReferencedSOPInstanceUID = SOPInstanceUID
            self.ContourImageSequence.append(contourImage)
        #print(type(self.ContourImageSequence))
        return self.ContourImageSequence


    def set_RTReferencedSeriesSequence(self, SeriesInstanceUID,ReferencedSOPClassUID, list_all_SOPInstanceUID):
        #self.RTReferencedSeriesSequence = pydicom.sequence.Sequence()
        self.RTReferencedSeries = pydicom.dataset.Dataset()
        self.RTReferencedSeries.SeriesInstanceUID = SeriesInstanceUID
        self.RTReferencedSeries.ContourImageSequence = self.set_ContourImageSequence(ReferencedSOPClassUID, list_all_SOPInstanceUID)
        #print(type(self.RTReferencedSeries))
        return self.RTReferencedSeries

    def set_RTReferencedStudySequence(self, StudyInstanceUID, SeriesInstanceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        self.RTReferencedStudy = pydicom.dataset.Dataset()
        self.RTReferencedStudy.StudyInstanceUID = StudyInstanceUID
        self.RTReferencedStudy.RTReferencedSeriesSequence = pydicom.sequence.Sequence()
        self.RTReferencedStudy.RTReferencedSeriesSequence.append(self.set_RTReferencedSeriesSequence(SeriesInstanceUID,ReferencedSOPClassUID, list_all_SOPInstanceUID))
        #print(type(self.RTReferencedStudy))
        return self.RTReferencedStudy

    def set_ReferencedFrameOfReferenceSequence(self, FrameOfReferenceUID, StudyInstanceUID, SeriesInstanceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        self.ReferencedFrameOfReference = pydicom.dataset.Dataset()
        self.ReferencedFrameOfReference.FrameOfReferenceUID = FrameOfReferenceUID
        self.ReferencedFrameOfReference.RTReferencedStudySequence = pydicom.sequence.Sequence()
        self.ReferencedFrameOfReference.RTReferencedStudySequence.append(self.set_RTReferencedStudySequence(StudyInstanceUID, SeriesInstanceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID))
        #print(type(self.ReferencedFrameOfReference))
        self.ReferencedFrameOfReferenceSequence.append(self.ReferencedFrameOfReference)

    def get_ReferencedFrameOfReferenceSequence(self):
        return self.ReferencedFrameOfReferenceSequence


    #ContourROISequence

    def set_ROIContourSequence(self, DisplayColor, ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData):
        self.ROIContour = pydicom.dataset.Dataset()
        roi_rtss = ROI_RTSS()
        roi_contour_sequence = roi_rtss.set_ROIContour(DisplayColor, ReferencedSOPClassUID, list_SOPInstanceUID, ContourGeometricType, list_ContourData)
        self.ROIContour = roi_contour_sequence 
        self.ROIContourSequence.append(self.ROIContour)

    def get_ROIContourSequence(self):
        return self.ROIContourSequence 
        
        



