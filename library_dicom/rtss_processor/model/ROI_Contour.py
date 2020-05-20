class ROI_Contour : 
    """a class to generate contour of a ROI as an object (for RoiContourSequence)
        / ensemble of contour on instance
    """

    def __init__(self, referenced_roi_number): #numero du ROI
        self.referenced_roi_number = referenced_roi_number


    def set_ROI_display_color(self,ROI_display_color): #couleur [255, 0,0] par ex
        self.ROI_display_color = ROI_display_color

    def set_referenced_SOP_class_UID(self, referenced_SOP_class_UID): #le même pour tout les rois 
        self.referenced_SOP_class_UID = referenced_SOP_class_UID

    def set_list_referenced_SOP_instance_UID(self, list_referenced_SOP_instance_UID): 
        """For a ROI, set list of SOP Instance UID(slice) in which there is a contour

        Arguments:
            list_referenced_SOP_instance_UID {list} -- [description]
        """
        self.list_referenced_SOP_instance_UID = list_referenced_SOP_instance_UID

    def set_contour_geometric_type(self, contour_geometric_type): #str
        self.contour_geometric_type = contour_geometric_type
    
    def set_list_number_of_contour_points(self, list_number_of_contour_points): #list de int 
        self.list_number_of_contours_points = list_number_of_contour_points

    def set_list_contour_data(self, list_contour_data): #list de liste de points des contours
        self.list_contour_data = list_contour_data


#methode get de mes infos pour y accéder 
    def get_ROI_display_color(self):
        return self.ROI_display_color
    
    def get_referenced_SOP_class_UID(self):
        return self.referenced_SOP_class_UID

    def get_list_referenced_SOP_instance_UID(self):
        return self.list_referenced_SOP_instance_UID

    def get_contour_geometric_type(self):
        return self.contour_geometric_type

    def get_list_number_of_contour_points(self):
        return self.list_number_of_contours_points
    
    def get_list_contour_data(self):
        return self.list_contour_data