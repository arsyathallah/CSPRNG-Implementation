from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np
import time


def generate_dynamic_sbox_time():
    """
    Generate a dynamic S-Box based on system time.
    """
    ts = int(time.time() * 1000)  # Current time in milliseconds
    random_values = [ts ^ (ts >> i) & 0xFF for i in range(8)]  # XOR shifting
    seed_value = sum(random_values) % (2**32)  # Ensure seed is within valid range
    sbox = list(range(256))
    np.random.seed(seed_value)  # Use XOR result as seed
    np.random.shuffle(sbox)  # Shuffle to create dynamic S-Box
    return sbox


def substitute_bytes_dynamic(block, sbox):
    """
    Perform substitution using the dynamic S-Box.
    """
    return bytes([sbox[b] for b in block])


def aes_encrypt_dynamic(plaintext, key, dynamic_sbox):
    """
    Encrypt plaintext using AES with a dynamic S-Box.
    Applies PKCS7 padding to plaintext.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)  # Apply padding
    substituted_plaintext = substitute_bytes_dynamic(padded_plaintext, dynamic_sbox)
    ciphertext = cipher.encrypt(substituted_plaintext)
    return ciphertext


def calculate_entropy(data):
    """
    Calculate the entropy of a data sequence.
    """
    data_array = np.frombuffer(data, dtype=np.uint8)
    frequencies = np.bincount(data_array, minlength=256) / len(data_array)
    entropy = -np.sum(frequencies * np.log2(frequencies + 1e-9))  # Avoid log(0)
    return entropy


# New feature for custom input
def custom_test():
    """
    Allow users to input plaintext for encryption or ciphertext for entropy calculation.
    """
    choice = input("Choose an option (1: Encrypt Plaintext, 2: Calculate Entropy of Ciphertext): ")

    if choice == "1":
        # Encrypt plaintext
        plaintext_input = input("Enter plaintext (up to 16 characters, will be padded if shorter): ")
        plaintext = plaintext_input.encode('utf-8')
        key_input = input("Enter 16-byte key: ")
        if len(key_input) != 16:
            print("Error: Key must be exactly 16 bytes.")
            return
        key = key_input.encode('utf-8')
        sbox = generate_dynamic_sbox_time()
        ciphertext = aes_encrypt_dynamic(plaintext, key, sbox)
        print("Ciphertext (Hex):", ciphertext.hex())
    elif choice == "2":
        # Calculate entropy of ciphertext
        ciphertext_hex = input("Enter ciphertext in hex format: ")
        try:
            ciphertext = bytes.fromhex(ciphertext_hex)
        except ValueError:
            print("Error: Invalid hex format.")
            return
        entropy = calculate_entropy(ciphertext)
        print("Entropy:", entropy)
    else:
        print("Invalid choice. Please choose either 1 or 2.")
