from dicom_to_cnn.model.petctviewer.Roi import Roi

class RoiNifti(Roi):
    """Derivated Class for automatic Nifti ROI of PetCtViewer.org

    Returns:
        [RoiNifti] -- Nifti ROI
    """

    def __init__(self, roi_number:int, list_point:list, volume_dimension:tuple):
        """constructor

        Args:
            roi_number (int): [roi number]
            list_point (list): [list of [x,y,z] coordonates ]
            volume_dimension (tuple): [(shape x, shape y, shape z)]
        """
        super().__init__(1, 0, 0, roi_number, 0, list_point, volume_dimension)
        self.list_points = self.calculateMaskPoint()

    def calculateMaskPoint(self) -> list:
        """Return [x,y,z] coordonates/voxel of nifti ROI (already in CSV file)

        Returns:
            [list]: [list of [x,y,z] coordonates of ROI ]
        """
        pixel_array = self.list_point
        list_points = []
        for points in pixel_array :
            if len(points) != 0 : 
                list_points.append(points)
        return list_points