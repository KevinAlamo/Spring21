def readKeys(filename, perm):
    keyFile = open(filename, perm)
    keys = []
    for i in range(8):
        keys.append(keyFile.read(1))

    keyFile.close()
    return keys

def readData(filename, perm):
    dataFile = open(filename,perm)
    data = []
    while(True):
        d = dataFile.read(2)
        if d == b'':
            break
    data.append(d)
    dataFile.close()
    return data


def desEncrypt(data, key):
    l = data[:1]
    r = data[1:]
    out_r = int.from_bytes(l, byteorder="big") ^ int.from_bytes(key, byteorder="big")
    out_l = r
    return out_l + out_r


def encrypt(input_data, keys):
    encrypted = []
    for data in input_data:
        for key in keys:
            data = desEncrypt(data, key)
        encrypted.append(data)
    return encrypted
