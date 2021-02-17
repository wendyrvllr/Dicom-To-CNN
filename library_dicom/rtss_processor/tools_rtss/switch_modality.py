def switch_modality(dict_coordonates, root_origin, target_origin):
    """[summary]

    Args:
        list_coordonates ([list]): dict of one ROIcoordonates to switch 
                                   {slice1 : [], slice2 : [], ...}
        root_origin ([list]): [IF CT to PET : ct origin [x,y,z], ELSE : pet origin ]
        target_origin ([list]): [IF CT to PET : pet origin [x,y,z], ELSE : ct_origin]
    """
    list_contour = []
    new_contour = dict_coordonates 
    number_of_slices = len(new_contour)
    delta = []
    for i in range(3):
        target_origin[i] = float(target_origin[i])
        root_origin[i] = float(root_origin[i])
        delta.append(root_origin[i] - target_origin[i])


    for i in range(number_of_slices):
        slice = new_contour[i]
        list_contour_slice = []
        for i in range(len(slice)):
            slice[i] = float(slice[i])
            if i%3 == 0 :
                slice[i] = slice[i] - delta[0]
                list_contour_slice.append(slice[i])
            elif i%3 == 1 : 
                slice[i] = slice[i] -  delta[1]
                list_contour_slice.append(slice[i])
            elif i%3 == 2 : 
                slice[i] = slice[i] - delta[2]
                list_contour_slice.append(slice[i])

        list_contour.append(list_contour_slice)
    return list_contour
