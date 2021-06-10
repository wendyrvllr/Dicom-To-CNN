from dicom_to_cnn.model.petctviewer.RoiPolygon import RoiPolygon
from dicom_to_cnn.model.petctviewer.RoiElipse import RoiElipse
from dicom_to_cnn.model.petctviewer.RoiNifti import RoiNifti
from dicom_to_cnn.model.petctviewer.Roi import Roi 


class RoiFactory():
    """Create ROI object from a CSV Roi details

    Returns:
        [RoiFactory] -- Factory for ROI instanciation according to csv details
    """

    def __init__(self, details:dict, volume_dimension:tuple, roi_number:int):
       """constructor

       Arguments:
           details {dict} -- Parsed ROI informations
           volume_dimension {tuple} -- Matrice dimension for Mask (should match DICOM input size, (shape x, shape y, shape z))
           roi_number {int} -- Integer number that will have to be written in the mask
       """
       self.details = details
       self.volume_dimension = volume_dimension
       self.roi_number = roi_number
    
    def read_roi(self) -> Roi:
        """Instanciate the Correct ROI type according to data

        Returns:
            [Roi] -- Roi object
        """
        first_slice = self.details['first_slice']
        last_slice = self.details['last_slice']
        point_list  = self.details['point_list']
        roi_number = self.roi_number
        type_number = self.details['type_number']
        volume_dimension = self.volume_dimension

        if (self.details['type_number'] == 1):
            return RoiPolygon( 1, first_slice, last_slice, roi_number, type_number, point_list, volume_dimension )

        elif (self.details['type_number'] == 11):
            return RoiElipse( 1, first_slice, last_slice, roi_number, type_number, point_list, volume_dimension )

        elif (self.details['type_number'] == 2):
            return RoiPolygon( 2, first_slice, last_slice, roi_number, type_number, point_list, volume_dimension )

        elif (self.details['type_number'] == 12):
            return RoiElipse( 2, first_slice, last_slice, roi_number, type_number, point_list, volume_dimension )

        elif (self.details['type_number'] == 3):
            return RoiPolygon( 3, first_slice, last_slice, roi_number, type_number, point_list, volume_dimension )

        elif (self.details['type_number'] == 13):
            return RoiElipse( 3, first_slice, last_slice, roi_number, type_number, point_list, volume_dimension )
        
        else:
            return RoiNifti( roi_number, point_list, volume_dimension )


    