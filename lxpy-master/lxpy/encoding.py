# -*- coding: utf-8 -*-

# TODO: b36\b62\b58\b91编码

import struct



# b36 看往上的说明，貌似应用于将数字转化成字符串进行保存？
def b36encode(num):
    alpha = '0123456789abcdefghijklmnopqrstuvwxyz'
    if not isinstance(num, int):
        raise TypeError('num must be an integer')
    if num < 0:
        return '-' + b36encode(-num)
    val = ''
    while num != 0:
        num, idx = divmod(num, len(alpha))
        val = alpha[idx] + val
    return val or '0'

def b36decode(val):
    return int(val, 36)

# s = b36encode(1111111111111111)
# print(s)
# s = b36decode(s)
# print(s)




def b62encode(num):
    alpha = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    if not isinstance(num, int):
        raise TypeError('num must be an integer')
    if num < 0:
        return '-' + b36encode(-num)
    val = ''
    while num != 0:
        num, idx = divmod(num, len(alpha))
        val = alpha[idx] + val
    return val or '0'

def b62decode(val):
    alpha = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    r = 0
    for idx,i in enumerate(val[::-1]):
        r += alpha.index(i) * (len(alpha) ** idx)
    return r

# s = b62encode(1111111111111111)
# print(s)
# s = b62decode(s)
# print(s)






base91_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$',
                   '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=',
                   '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '"']

decode_table = dict((v, k) for k, v in enumerate(base91_alphabet))

def b91decode(encoded_str):
    ''' Decode Base91 string to a bytearray '''
    v = -1
    b = 0
    n = 0
    out = b''
    for strletter in encoded_str.decode():
        if not strletter in decode_table:
            continue
        c = decode_table[strletter]
        if (v < 0):
            v = c
        else:
            v += c * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            while True:
                out += struct.pack('B', b & 255)
                b >>= 8
                n -= 8
                if not n > 7:
                    break
            v = -1
    if v + 1:
        out += struct.pack('B', (b | v << n) & 255)
    return out

def b91encode(bindata):
    ''' Encode a bytearray to a Base91 string '''
    b = 0
    n = 0
    out = ''
    for count in range(len(bindata)):
        byte = bindata[count:count + 1]
        b |= struct.unpack('B', byte)[0] << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out += base91_alphabet[v % 91] + base91_alphabet[v // 91]
    if n:
        out += base91_alphabet[b % 91]
        if n > 7 or b > 90:
            out += base91_alphabet[b // 91]
    return out.encode()

# 统一输入输出的格式
# s = b91encode(b'asdfasdf')
# print(s)
# s = b91decode(s)
# print(s)



# b58
# 没有0，大写的O，大写的I，以及小写的l
alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
alphalen = len(alphabet)

def b58encode_int(i, default_one=True):
    '''Encode an integer using Base58'''
    if not i and default_one:
        return alphabet[0:1]
    string = b""
    while i:
        i, idx = divmod(i, alphalen)
        string = alphabet[idx:idx+1] + string
    return string

def b58encode(v):
    nPad = len(v)
    v = v.lstrip(b'\0')
    nPad -= len(v)
    p, acc = 1, 0
    for c in reversed(v):
        acc += p * c
        p = p << 8
    result = b58encode_int(acc, default_one=False)
    return (alphabet[0:1] * nPad + result)

def b58decode_int(v):
    decimal = 0
    for char in v:
        decimal = decimal * alphalen + alphabet.index(char)
    return decimal

def b58decode(v):
    origlen = len(v)
    v = v.lstrip(alphabet[0:1])
    newlen = len(v)
    acc = b58decode_int(v)
    result = []
    while acc > 0:
        acc, mod = divmod(acc, 256)
        result.append(mod)
    return (b'\0' * (origlen - newlen) + bytes(reversed(result)))


# s = b58encode(b'asdfasdf')
# print(s)
# s = b58decode(s)
# print(s)
