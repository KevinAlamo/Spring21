import sys


def readKeys(filename, perm):
    keyFile = open(filename, perm)
    keys = []
    for i in range(8):
        keys.append(keyFile.read(1))
    keyFile.close()
    return keys


def readData(filename, perm):
    dataFile = open(filename, perm)
    data = []
    while(True):
        d = dataFile.read(2)
        if d == b'':
            break
        data.append(d)
    dataFile.close()
    return data


def desDecrypt(data, key):
    l = data[:1]
    r = data[1:]
    out_l = int.from_bytes(r, byteorder="big") ^ int.from_bytes(key, byteorder="big")
    out_l = out_l.to_bytes(1, byteorder="big")
    out_r = l
    return out_l + out_r


def decrypt(input_data, keys):
    encrypted = []
    for data in input_data:
        for key in keys:
            data = desDecrypt(data, key)
        encrypted.append(data)
    return encrypted


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('No key or data file')

    keys = readKeys(sys.argv[1], 'rb')
    data = readData(sys.argv[2], 'rb')
    decrypted = decrypt(data, keys)
    file = open('decrypted_text.txt', 'wb')
    for c in decrypted:
        file.write(c)
    file.close()
