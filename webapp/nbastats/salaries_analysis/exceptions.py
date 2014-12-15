__author__='Yi Liu'

class Error(Exception):
    pass

class cannotLoadDataError(Error):
    """Raise this error when data file is missing"""

    def __init__(self,msg):
        self.msg = msg
        print self.msg
    pass

