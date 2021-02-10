def readKeys(filename, perm):
    keyFile = open(filename, perm)
    keys = []
    for i in range(8):
        keys.append(keyFile.read(1))

    keyFile.close()
    return keys
