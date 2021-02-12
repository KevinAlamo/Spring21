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


def desEncrypt(dat, key):
    l = dat[:1]
    r = dat[1:]
    out_r = int.from_bytes(l, byteorder="big") ^ int.from_bytes(key, byteorder="big")
    out_r = out_r.to_bytes(1, byteorder="big")
    out_l = r
    return out_l + out_r

# encrypts the data
def encrypt(input_data, keys):
    encrypted = []
    odd = 0
    for text in input_data:
        if len(text) == 1:  # case for padding
            text = text + b' '
            odd = 1
        for key in keys:
            text = desEncrypt(text, key)
        if odd == 1:
            encrypted.append(text[:1])
        else:
            encrypted.append(text)
    return encrypted


def outputFile(encrypted_text):
    file = open('encrypted_text.txt', 'wb')
    for c in encrypted_text:
        file.write(c)
    file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('No key or data file')

    keys = readKeys(sys.argv[1], 'rb')
    data = readData(sys.argv[2], 'rb')
    encrypted = encrypt(data, keys)
    outputFile(encrypted)
