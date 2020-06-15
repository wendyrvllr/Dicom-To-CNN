#une classe pour récupérer le nom, description, calcul volume de chaque ROI pour le remplir avec des set
#dans RTSS_writer 
import pydicom 
import numpy as np

#voir si pour 1 ROI ou boucle sur toute les ROI 

class Data_ROI_RTSS : 

    def __init__(self, mask_3D):
        self.mask_3D = mask_3D
        self.StructureSetROISequence = pydicom.sequence.Sequence()


    def set_data_roi(self,pixel_spacing, ROINumber, ReferencedFrameOfReferenceUID, ROIName) :
        structure_set_roi = pydicom.dataset.Dataset()
        structure_set_roi.ROINumber = ROINumber
        structure_set_roi.ReferencedFrameOfReferenceUID = ReferencedFrameOfReferenceUID
        structure_set_roi.ROIName = ROIName
        structure_set_roi.ROIVolume = self.get_roi_volume(pixel_spacing)
        structure_set_roi.ROIGenerationAlgorithm = 'SEMIAUTOMATIC' #OU MANUAL 
        self.StructureSetROISequence.append(structure_set_roi)

    def get_roi_volume(self, pixel_spacing):
        number_pixel = 0
        for z in range(self.mask_3D[2]):
            for y in range(self.mask_3D[1]):
                for x in range(self.mask_3D[0]):
                    if self.mask_3D[x,y,z] != 0 : 
                        number_pixel += 1
        volume_pixel = pixel_spacing[0] * pixel_spacing[1] * abs(pixel_spacing[2])
        volume_pixel = volume_pixel * 10**(-3) #mm3 to ml 
        roi_volume = number_pixel * volume_pixel 

        return np.round(roi_volume , 5)

