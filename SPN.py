#!/bin/python3

import sbox
import pbox
import keygen


def encrypt(plain_text, key, prime, stage):
    # print(f"--- Beginning stage {stage} encryption ---")
    print("plain text = ", plain_text)

    # print("substage 1: pbox.encrypt")
    e_text_1 = pbox.encrypt(plain_text, prime)
    # print("e text of pbox = ", e_text_1)

    # print("substage 2, sbox.encrypt")
    e_text_2 = sbox.substitute_encrypt(e_text_1, key)
    # print("e text of sbox = ", e_text_2)

    return e_text_2


def decrypt(plain_text, encrypted_text, key, prime, stage):
    # print(f"--- Beginning stage {stage} decryption ---")
    # print("decrypting sbox")
    d_text_2 = sbox.substitute_decrypt(encrypted_text, key)
    # print("d text of sbox = ", d_text_2)

    padding = pbox.padding(plain_text, prime)
    # print("decrypting pbox")
    d_text_1 = pbox.decrypt(d_text_2, prime, padding)
    # print("d text of pbox = ", d_text_1)

    return d_text_1


def main():
    key_list = []
    key = keygen.generate_final_key()
    key_list.append(key[:100])
    key_list.append(key[100:])

    stages = int(input("how many stages? > "))
    print("stages = ", stages)
    for i in range(stages):
        key_list.append(sbox.substitute_encrypt(key_list[i+1], key_list[1]))
    print("key list = ", key_list)
    rev_key_list = key_list[::-1]

    primes = keygen.list_primes(stages)
    print("primes = ", primes)
    rev_primes = primes[::-1]

    plain_text = "hellow how do you do? I am doing fine, thank you. What about you? I am also doing fine."

    encrypted_text = []
    encrypted_text.append(plain_text)

    for i in range(stages):
        encrypted_text.append(encrypt(encrypted_text[i], key_list[i+1], primes[i], i+1))
        print(f"encrypted stage {i+1} text = ", encrypted_text[i+1])

    # encrypted_text.append(encrypt(encrypted_text[0], key_list[1], primes[0], 1))
    # print("encrypted stage 1 text = ", encrypted_text[1])

    # encrypted_text.append(encrypt(encrypted_text[1], key_list[2], primes[1], 2))
    # print("encrypted stage 2 text = ", encrypted_text[2])

    print("\n========================================\n")

    decrypted_text = []
    decrypted_text.insert(0, encrypted_text[-1])
    print("text to be decypted = ", decrypted_text[0])

    for i in range(stages, 0, -1):
        decrypted_text.insert(0, decrypt(encrypted_text[i-1], encrypted_text[i], key_list[i], primes[i-1], i))
        print(f"decrypted stage {i} text = ", decrypted_text[0])

    # decrypted_text.insert(0, decrypt(encrypted_text[1], encrypted_text[2], key_list[2], primes[1], 2))
    # print("decrypted stage 2 text = ", decrypted_text[0])

    # decrypted_text.insert(0, decrypt(encrypted_text[0], encrypted_text[1], key_list[1], primes[0], 1))
    # print("decrypted stage 1 text = ", decrypted_text[0])


if __name__ == '__main__':
    main()
