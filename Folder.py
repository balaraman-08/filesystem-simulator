class Folder:
    """This class is used simulate a folder structure"""
    name = ""
    parent = None
    children = None
    path = ""

    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent
        self.children = []
        if not parent:
            self.path = name
        else:
            self.path = "{}\\{}".format(parent.path, name)

    # This function returns the name of the Folder
    # when str() function is called on a Folder instance
    def __str__(self):
        return self.name

    # addChild() function takes Folder or File instance
    # as child and appends it to child list
    def addChild(self, newChild):
        if self.isChildPresent(newChild.name):
            raise Exception("Folder or File  already exists")
        self.children.append(newChild)
        return True

    # getChildren() will return the list of its
    # child files and folders
    def getChildren(self):
        return self.children

    # getChild() takes a string as parameter
    # Returns Folder or File instance if there is a child with given name
    # Otherwise returns False
    def getChild(self, childName: str):
        for child in self.children:
            if child.name == childName:
                return child
        return False

    # deleteChildren() takes File or Foldername as parameter
    # and removes corresponding file or folder from children list
    # if exists
    def deleteChildren(self, childToDelete):
        for idx, child in enumerate(self.children):
            if child.name == childToDelete.name:
                self.children.pop(idx)
                return True
        return False

    # isChildPresent() takes a string as parameter
    # Returns True if there is a child with given name
    # Otherwise returns False
    def isChildPresent(self, childName: str):
        for child in self.children:
            if child.name == childName:
                return True
        return False