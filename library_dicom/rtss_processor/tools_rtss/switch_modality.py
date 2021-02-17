def switch_modality(list_coordonates, root_origin, target_origin):
    """[summary]

    Args:
        list_coordonates ([list]): list of ROIs coordonates to switch 
                                    [ ['roi1 [slice1], [slice[2], ..], ['roi2 [slice1], [slice[2], ..], ...]
        root_origin ([list]): [IF CT to PET : ct origin [x,y,z], ELSE : pet origin ]
        target_origin ([list]): [IF CT to PET : pet origin [x,y,z], ELSE : ct_origin]
    """

    new_contour = list_coordonates 
    delta = []
    for i in range(3):
        target_origin[i] = float(target_origin[i])
        root_origin[i] = float(root_origin[i])
        delta.append(root_origin[i] - target_origin[i])

    for roi in new_contour : 
        for slice in roi :
            for i in range(len(slice)):
                slice[i] = float(slice[i])
                if i%3 == 0 :
                    slice[i] = slice[i] - delta[0]

                elif i%3 == 1 : 
                    slice[i] = slice[i] -  delta[1]

                elif i%3 == 2 : 
                    slice[i] = slice[i] - delta[2]


    return new_contour 
