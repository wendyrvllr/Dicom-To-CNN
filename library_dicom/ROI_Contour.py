class ROI_Contour : 
    """a class to generate contour of a ROI as an object (for RoiContourSequence)
    """

    def __init__(self):
        pass


    def set_ROI_display_color(self,ROI_display_color):
        self.ROI_display_color = ROI_display_color

    def set_referenced_roi_number(self,referenced_roi_number):
        self.referenced_roi_number = referenced_roi_number

    def set_referenced_SOP_class_UID(self, referenced_SOP_class_UID):
        self.referenced_SOP_class_UID = referenced_SOP_class_UID

    def set_referenced_SOP_instance_UID(self, referenced_SOP_instance_UID):
        self.referenced_SOP_instance_UID = referenced_SOP_instance_UID

    def set_contour_geometric_type(self, contour_geometric_type):
        self.contour_geometric_type = contour_geometric_type
    
    def set_number_of_contour_points(self, number_of_contour_points):
        self.number_of_contours_points = number_of_contour_points

    def set_contour_data(self, contour_data):
        self.contour_date = contour_data