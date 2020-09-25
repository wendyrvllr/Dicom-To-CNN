from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader


def get_sum_rois_volume(liste):
    volume = float(0)
    for i in range(len(liste)):
        volume += float(liste[i][3])

    return volume


def get_difference_volume(csv_path) :
    csv_objet = CsvReader(csv_path)
    total_volume = float(csv_objet.get_sum_row()[3])

    liste = csv_objet.get_rois_results()

    sum_volume = get_sum_rois_volume(liste)
    return total_volume, sum_volume, abs(sum_volume - total_volume)


