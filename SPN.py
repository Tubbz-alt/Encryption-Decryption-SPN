#!/bin/python3

import sbox
import pbox
import keygen


def encrypt(plain_text, key, prime, stage):
    print("plain text = ", plain_text)
    e_text_1 = pbox.encrypt(plain_text, prime)
    e_text_2 = sbox.substitute_encrypt(e_text_1, key)
    return e_text_2


def decrypt(plain_text, encrypted_text, key, prime, stage):
    d_text_2 = sbox.substitute_decrypt(encrypted_text, key)
    padding = pbox.padding(plain_text, prime)
    d_text_1 = pbox.decrypt(d_text_2, prime, padding)
    return d_text_1


def main():
    key_list = []
    key = keygen.generate_final_key()
    key_list.append(key[:100])
    key_list.append(key[100:])

    stages = int(input("how many stages? > "))
    for i in range(stages):
        key_list.append(sbox.substitute_encrypt(key_list[i+1], key_list[1]))

    primes = keygen.list_primes(stages)
    print("key = ", key)
    print("primes = ", primes)
    print("\n========================================\n")

    plain_text = "hellow how do you do? I am doing fine, thank you. What about you? I am also doing fine."

    encrypted_text = []
    encrypted_text.append(plain_text)

    print("--- Encryption ---")
    for i in range(stages):
        encrypted_text.append(encrypt(encrypted_text[i], key_list[i+1], primes[i], i+1))
        print(f"encrypted stage {i+1} text = ", encrypted_text[i+1])

    print("\n========================================\n")

    decrypted_text = []
    decrypted_text.insert(0, encrypted_text[-1])
    print("--- Decryption ---")
    print("text to be decypted = ", decrypted_text[0])

    for i in range(stages, 0, -1):
        decrypted_text.insert(0, decrypt(encrypted_text[i-1], encrypted_text[i], key_list[i], primes[i-1], i))
        print(f"decrypted stage {i} text = ", decrypted_text[0])


if __name__ == '__main__':
    main()
