class IDataStructure:

    def __init__(self):
        pass

    def PrintString(self):
        print(" ".join([k + " {}".format(v) for k, v in vars(self).items()]))