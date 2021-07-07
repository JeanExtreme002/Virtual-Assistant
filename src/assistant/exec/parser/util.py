def sort_dict(dict_obj, key = None, reverse = False):
    new_dict = dict()

    for key in sorted(dict_obj, key = key, reverse = reverse):
        new_dict[key] = dict_obj[key]
    return new_dict
