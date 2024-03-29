import sys

# reads in the keys with given permissions
def readKeys(filename, perm):
    keyFile = open(filename, perm)
    keys = []
    for i in range(8):
        keys.append(keyFile.read(1))
    keyFile.close()
    return keys


# reads in the data
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


# DES decryption method
def desDecrypt(data, key):
    l = data[:1]
    r = data[1:]
    out_l = int.from_bytes(r, byteorder="big") ^ int.from_bytes(key, byteorder="big")
    out_l = out_l.to_bytes(1, byteorder="big")
    out_r = l
    return out_l + out_r


# method that runs the decryption
def decrypt(input_data, keys):
    encrypted = []
    odd = 0
    for data in input_data:
        if len(data) == 1:  # case for padding
            data = data + b' '
            odd = 1
        for key in keys:
            data = desDecrypt(data, key)
        if odd == 1:  # removes the padding if it has it
            encrypted.append(data[:1])
        else:
            encrypted.append(data)
    return encrypted


# writes to the output file
def outfile(decrypted_text):
    file = open('decrypted_text.txt', 'wb')
    for c in decrypted_text:
        file.write(c)
    file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('No key or data file')

    keys = readKeys(sys.argv[1], 'rb')
    data = readData(sys.argv[2], 'rb')
    decrypted = decrypt(data, keys)
    outfile(decrypted)
