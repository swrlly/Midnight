class IDataStructure:

    def __init__(self):
        pass

    def PrintString(self):
        itr = vars(self).items()
        baseTypes = set([str, float, int, list])
        print(" ".join([k + " {}".format(v) for k, v in itr if type(v) in baseTypes]))
        for k, v in itr:
            if type(v) not in baseTypes: v.PrintString()