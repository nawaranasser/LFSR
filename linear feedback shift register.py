from operator import xor


def txt_to_ascii(txt):
    ascii_list = []
    for char in txt:
        ascii_list.append(ord(char))
    return ascii_list


def ascii_to_txt(ascii_list):
    txt = " "
    for value in ascii_list:
        txt += chr(value)
    return txt


def shifting(initial_vector):
    shifted_reg = initial_vector.copy()
    shifted_reg.insert(0, 0)
    shifted_reg.pop()
    return shifted_reg


def xoring(poly, vec):
    feedback_bit = vec[poly[0]]
    for x in range(1, len(poly)):
        feedback_bit = xor(feedback_bit, vec[poly[x]])
    return feedback_bit


def getKey(initial_vector):
    shifted_reg = initial_vector.copy()
    shifted_reg.insert(0, 0)
    pop_bit = shifted_reg.pop()
    return pop_bit


def lfsr(initial_vector, poly, m):
    num_clk = (2 ** m)
    key = []
    for i in range(num_clk):
        if i == 0:
            shifted_vector = shifting(initial_vector)
            feedback = xoring(poly, initial_vector)
            shifted_vector[0] = feedback
            k = getKey(initial_vector)
            key.append(k)
        else:
            shifted_vector = shifting(shifted_vector)
            feedback = xoring(poly, shifted_vector)
            shifted_vector[0] = feedback
            k = getKey(shifted_vector)
            key.append(k)
    return key


def encryption(plain_txt_):
    plain_txt_ = txt_to_ascii(plain_txt_)
    key = lfsr([1, 0, 0], [1, 2], 3)
    for _ in range(len(plain_txt_)):
        if len(key) <= len(plain_txt_):
            key = key + key
    cipher_txt = []
    for bit in range(len(plain_txt_)):
        cipher_txt.append(xor(plain_txt_[bit], key[bit]))
    return cipher_txt


def decryption(cipher_txt, poly, m):
    # init_vector = cipher_txt[:(2 ** m)]
    # print(init_vector)
    key2 = lfsr([1, 0, 0], poly, m)
    for _ in range(len(cipher_txt)):
        if len(key2) <= len(cipher_txt):
            key2 = key2 + key2
    plain_txt_ = []
    for bit in range(len(cipher_txt)):
        plain_txt_.append(xor(cipher_txt[bit], key2[bit]))
    return ascii_to_txt(plain_txt_)


plain_txt = input("Enter the plaintext: ")
encrypted_txt = encryption(plain_txt)
print("Encrypted Text: ", ascii_to_txt(encrypted_txt))
print("ascii of encrypted text: ", encrypted_txt)
decrypted_txt = decryption(encrypted_txt, [1, 2], 3)
print("Decrypted Text:", decrypted_txt)
# ---------------------------------------
# encrypt (plain_txt)
# converter = convert(plain_txt) form letter to ascii
# key1 = lfsr(initial_vector, poly, m)
# key2 = repeat key1 along to converter
# cipher_txt = converter xor key2
# encrypted_txt = convert(cipher_txt) form ascii to letter
# return encrypted_txt
#
# decrypt(encrypted_txt, m, poly)
# converter = convert(encrypted_txt) form letter to ascii
# key_len = 2^m
# converter[0: key_len] = key1
# key2 = lfsr(key1, poly, m)
# plain_txt = converter xor key2
# decrypted_txt = convert(plain_txt) form ascii to letter
# return decrypted_txt
