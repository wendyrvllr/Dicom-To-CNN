import csv

class CsvReader():
    """Read CSV file from petctviewer.org
    """

    def __init__(self, path):
        self.path=path
        self.__load_data()

    def __load_data(self):
        """Load data in this object, during reading, search
        for manual and automatic (nifti) roi declaration part
        """
        with open(self.path, 'r') as csvfile : 
            reader = csv.reader(csvfile)
            csv_data = []
            index = 0
            for row in reader :
                if(row and 'Number of ROIs = ' in row[0]) :
                    number_of_manual_roi = row[0].replace("Number of ROIs = ", "").strip()
                    self.first_line_manual_roi = index
                    self.number_of_manual_roi = int(number_of_manual_roi)
                if(row and 'Number of Nifti ROIs = ' in row[0]) :
                    number_of_nifti_roi = row[0].replace("Number of Nifti ROIs = ", "").strip()
                    self.first_line_nifti_roi = index
                    self.number_of_nifti_roi = int(number_of_nifti_roi)
                csv_data.append(row) #liste de liste(chaque ligne = liste)
                index += 1

        self.csv_data = csv_data
    
    def get_manual_rois(self):
        """return manual rois block
        """
        try :
            first_manual_roi = self.first_line_manual_roi + 1
        except AttributeError:
            return
        last_manual_row =  first_manual_roi + self.number_of_manual_roi
        return self.csv_data[ first_manual_roi : last_manual_row ]
    
    def get_nifti_rois(self):
        """ return automatic (nifti) roi block
        """
        try :
            first_nifti_row = self.first_line_nifti_roi + 1
        except AttributeError:
            return
        last_nifti_row = first_nifti_row + self.number_of_nifti_roi
        return self.csv_data[ first_nifti_row : last_nifti_row ]

    @classmethod 
    def convert_manual_row_to_object(cls, manual_row):
        """Return a row manual row in an object with ROI details

        Arguments:
            manual_row {list} -- raw, row manual row

        Returns:
            [object] -- object describing the row
        """
        number_point_field = manual_row[4]
        number_point = int( number_point_field.replace(" num points = ", "").strip() )
        point_list_string = manual_row[ 5 : (5 + number_point) ]
        point_list = CsvReader.list_string_to_point_list_int( point_list_string )

        result_answer = {
                'name' : manual_row[0].strip(),
                'first_slice' : int(manual_row[2].strip()),
                'last_slice' : int(manual_row[3].strip()),
                'type_number' : int(manual_row[1].strip()),
                'point_list' : point_list
        }

        return result_answer


    @classmethod
    def convert_nifti_row_to_list_point(cls, nifti_row):
        """Return list of point included in the roi

        Arguments:
            nifti_row {list} -- nifti row of the csv

        Returns:
            [list] -- list of point in the roi
        """
        point_list_string = nifti_row[2:]
        point_list = CsvReader.list_string_to_point_list_int( point_list_string )
        result_answer = {
                'name' : nifti_row[0].strip(),
                'first_slice' : 0,
                'last_slice' : 0,
                'type_number' : 0,
                'point_list' : point_list
        }
        return result_answer

    @classmethod
    def list_string_to_point_list_int(cls, point_list_string):
        """
        Transforms point string into list of coordinate (int)
        """
        point_list_string = list(map(str.strip, point_list_string))
        point_list = []
        for point_string in point_list_string:
            list_string_point = point_string.split()
            list_int_point = list(map(int, list_string_point))
            point_list.append(list_int_point)
        return point_list


        