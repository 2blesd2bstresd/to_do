def serialize(self):
    return_list = [type(None), float, int, bool]
    output = {}
    for k, v in self.__dict__.iteritems():
        if type(v) in return_list:
            output[k] = v
        else:
            try:
                output[k] = v.__str__()
            except:
                output[k] = v.encode("utf8")
    return output