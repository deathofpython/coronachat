def hash_algorythm(string):
    hash = ''
    for i in string:
        hash += chr(ord(i) + 10)
    return hash