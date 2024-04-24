def  store_objects(problem):
    dict_obj = {}
    for object in problem.objects:
        key = next(iter(object.type_tags))
        if key not in dict_obj:
            dict_obj[key] = []
        dict_obj[key].append(repr(object)[9:-1])
    return dict_obj