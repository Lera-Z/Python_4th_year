class UniqObject:
    class Helper:
        def __init__(self, arg):
            self.val = arg

    instance = None

    def __init__(self, arg):
        if not UniqObject.instance:
            UniqObject.instance = UniqObject.Helper(arg)
        else:
            UniqObject.instance.val = arg

    @classmethod
    def create_object(cls, arg):
        if not UniqObject.instance:
            UniqObject.instance = UniqObject.Helper(arg)
        else:
            UniqObject.instance.val = arg
        return UniqObject.instance
