class Parser(object):
    """
    Executes processors ordered by the list
    """

    def __init__(self, processors):
        self.processors = processors

    def follow(self, callback, request, env={}):
        processor = self.processors.pop(0)
        return processor.execute(callback, self, request, env)
