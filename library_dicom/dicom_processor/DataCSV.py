import csv

class DataCSV():
    """[summary]
    """

    def __init__(self, path):
        self.path=path
        self.__load_data()

    def __load_data(self):
        with open(self.path, 'r') as csvfile : 
            reader = csv.reader(csvfile)
            csv_data = []
            for row in reader : 
                csv_data.append(row) #liste de liste(chaque ligne = liste)

        nb_line = len(csv_data) #nbr de lignes

        for i in range(nb_line) : 
            if (len(csv_data[i] == 0)):
                csv_data = csv_data[i+1:nb_line]
                break

        return csv_data

    # return le deuxieme bloc du fichier csv pour les ROI
    #sous cette forme 
    #[['Number of ROIs = 4'], 
    # ['31 - Urinary system', ' 1', ' 85', ' 134', ' num points = 9', ' 111 68', ' 103 58', ' 82 57', ' 69 69', ' 73 94', ' 88 109', ' 101 106', ' 106 97', ' 109 79'], 
    # ['Urinary system', ' 1', ' 98', ' 141', ' num points = 8', ' 73 99', ' 72 83', ' 71 74', ' 55 67', ' 42 73', ' 42 93', ' 47 110', ' 63 113'],
    #  ['6 - Mediastinal', ' 11', ' 143', ' 171', ' num points = 3', ' 87 86', ' 101 86', ' 87 72'],
    #  ['Mediastinal', ' 11', ' 154', ' 172', ' num points = 3', ' 95 72', ' 104 72', ' 95 63'], 
    # ['SUVlo', ' SUVhi', ' CTlo', ' CThi', ' useSUV', ' useCT', ' CtRadio'], 
    # ['41%', ' 100', ' -1000', ' 1000', ' 1', ' 0', ' 2']]


    #idée 2 
    def __load_data(self):
        with open(self.path, 'r') as csvfile : 
            reader = csv.reader(csvfile)
            for row in reader : 
                print(row) #print la ligne 
                for i in range(len(row)):
                    print(row[i]) #print tous les éléments de chaque lignes 

    #de la forme : 
    #['31 - Urinary system', ' 1', ' 85', ' 134', ' num points = 9', ' 111 68', ' 103 58', ' 82 57', ' 69 69', ' 73 94', ' 88 109', ' 101 106', ' 106 97', ' 109 79']
    #31 - Urinary system
    #1
    #85
    #134
    #num points = 9
    #111 68
    #103 58
    #82 57
    #69 69
    #73 94
    #88 109
    #101 106
    #106 97
    #109 79

        