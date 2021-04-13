import sys

from Folder import Folder
from File import File

currentFolder = Folder("Root:", None)

# mkdir
def mkdir(*args):
    global currentFolder
    
    # Maximum arguments allowed is 1
    if (len(args) != 1):
        print("Invalid usage")
        return False

    name = args[0]

    # check if folder already exists
    # if present, return false
    # otherwise create a folder
    if currentFolder.isChildPresent(name):
        print("Folder name already exists")
        return False
    newFolder = Folder(name, currentFolder)
    currentFolder.addChild(newFolder)
    print("{} created".format(name))

# cd
def cd(*args):
    global currentFolder

    # Maximum arguments allowed is 1
    if (len(args) != 1):
        print("Invalid usage")
        return False

    path = args[0].split('/')

    sourceFolder = currentFolder
    for folder in path:
        # If the path contains ..
        # Move to parent folder 
        # if parent folder is None, then already in root folder
        if folder == "..":
            sourceFolder = sourceFolder.parent
            if not sourceFolder:
                print("Path does not exist")
                return False
            continue

        sourceFolder = sourceFolder.getChild(folder)
        if not sourceFolder:
            print("Path does not exist")
            return False

    if isinstance(sourceFolder, Folder):
        currentFolder = sourceFolder
        return True
    else:
        print("Destination is not a folder")
        return False

# delete
def delete(*args):
    global currentFolder

    # Maximum arguments allowed is 1
    if (len(args) != 1):
        print("Invalid usage")
        return False

    path = args[0]

    child = currentFolder.getChild(path)
    if not child:
        print("Folder or File name does not exists")
        return False
    elif isinstance(child, Folder):
        confirmation = input("Do you want to delete {} along with its sub folders and files? (Y/n) ".format(path))
        if confirmation.lower() == "n":
            print("Operation cancelled")
            return False
    
    if currentFolder.deleteChildren(child):
        print("{} deleted successfully".format(path))
        return True
    else:
        print("Unexpected Error occured")
        return False

# echo
def echo(*args):
    global currentFolder

    content = []
    indexOfSeparator = -1
    for idx, arg in enumerate(args):
        if arg == '>':
            indexOfSeparator = idx
            break
        else:
            content.append(arg)

    # Join the list of strings into space separated string
    content = ' '.join(content)

    # > symbol should be second from last argument
    # otherwise invalid usage
    if indexOfSeparator == -1:
        print(content)
        return True
    elif indexOfSeparator != len(args) - 2:
        print("Invalid usage")
        return False
    else:
        filename = args[-1]
        child = currentFolder.getChild(filename)
                
        # Check if the file is already present
        # if not present, create a file
        if not child:
            newFile = File(filename, currentFolder, content)
            currentFolder.addChild(newFile)
            print("{} created".format(filename))
            return True
        else:
            # if fiel present, ask confirmation to overwrite
            confirmation = input("File {} already exists. Do you want to overwrite? (Y/n) ".format(filename))
            if confirmation.lower() == "n":
                print("Operation cancelled")
                return False
            else:
                # Overwrite the write
                child.writeContents(content)
                print("File overwritten")
                return True

# cat
def cat(*args):
    global currentFolder
    # Arguments allowed either 1 or 3
    if len(args) == 1:
        filename = args[0]
        child = currentFolder.getChild(filename)
        
        if not child or not isinstance(child, File):
            print("File name does not exists")
            return False
        
        print(child.getContents())
        return True
    elif len(args) == 3:
        if args[1] != '>':
            print('Invalid usage')
            return False
        sourceFileName = args[0]
        destinationFileName = args[2]
        
        # Check if source file is present
        # if not, return False
        sourceFile = currentFolder.getChild(sourceFileName)
        if not sourceFile or not isinstance(sourceFile, File):
            print("Source File {} does not exists".format(sourceFile))
            return False

        # Check if destination file is present
        # if present, ask for confirmation
        # if not present, create a new file
        destinationFile = currentFolder.getChild(destinationFileName)
        if destinationFile and isinstance(sourceFile, File):
            confirmation = input("Destination File {} already exists. Do you want to overwrite? (Y/n) ".format(sourceFile))
            if confirmation.lower() == "n":
                print("Operation cancelled")
                return False
            else:
                # Overwrite the write
                destinationFile.writeContents(sourceFile.getContents())
                print("File overwritten")
                return True
        else:
            destinationFile = File(destinationFileName, sourceFile.parent, sourceFile.getContents())  
            currentFolder.addChild(destinationFile)   
            return True

# wc
def wordCount(*args):
    # Maximum arguments allowed is 1
    if len(args) == 1:
        filename = args[0]
        child = currentFolder.getChild(filename)
        
        if not child or not isinstance(child, File):
            print("File name does not exists")
            return False
        else:
            contents = child.getContents()
            print("Line count: {}\nWord count: {}\nCharacter count: {}".format(
                len(contents.split('\n')),
                len(contents.split()),
                len(contents)
            ))
    else:
        print("Invalid usage")
        return False

# dir
def dir():
    global currentFolder
    children = currentFolder.getChildren()
    print("{}   {} {}".format(
            "Type".ljust(6,' '),
            "Name".ljust(20, ' '),
            "Size",
    ))
    print("".ljust(38, '-'))
    for child in children:
        if isinstance(child, File):
            print("{} - {} {} Bytes".format(
            "File".ljust(6,' '),
            child.name.ljust(20, ' '),
            len(child.getContents())
            ))
        else:
            print("{} - {} {}".format(
            "Folder",
            child.name.ljust(20, ' '),
            len(child.getChildren())
            ))


# pwd
def pwd():
    global currentFolder
    print(currentFolder.path)

# exit
def exit():
    sys.exit(0)

# commands dictionary contains the function name
# and argument count for each command
commands = {
    "mkdir": {
        "function": mkdir,
        "argCount": 1,
    },
    "cd": {
        "function": cd,
        "argCount": 1,
    },
    "echo": {
        "function": echo,
        "argCount": 3,
    },
    "cat": {
        "function": cat,
        "argCount": 3,
    },
    "wc": {
        "function": wordCount,
        "argCount": 1,
    },
    "del": {
        "function": delete,
        "argCount": 1,
    },
    "pwd": {
        "function": pwd,
        "argCount": 0,
    },
    "dir": {
        "function": dir,
        "argCount": 0,
    },
    "exit": {
        "function": exit,
        "argCount": 0,
    },
}

# Driver Code
while True:
    cmd = input("\n{}>".format(currentFolder.path)).split()
    if cmd[0] not in commands:
        print("Invalid command")
    elif cmd[0] == "exit":
        exit()
    else:
        command = commands[cmd[0]]
        commandFuntion = command["function"]

        if command["argCount"] == 0:
            commandFuntion()
        elif command["argCount"] >= 1:
            commandFuntion(*cmd[1:])