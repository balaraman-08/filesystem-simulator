class File:
    """This class is used simulate a file"""
    name = ""
    parent = None
    contents = ""
    def __init__(self, name, parent, contents):
        self.name = name
        self.parent = parent
        self.contents = contents

    # This function returns the name of the File
    # when str() function is called on a File instance
    def __str__(self):
        return self.name

    def getContents(self):
        return self.contents
    
    def writeContents(self, newContents):
        self.contents = newContents