import timebased_aes as time_aes
import butterflybased_aes as butterfly_aes
import logging
import time
import argparse
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def compare_encryption(plaintext, key):
    """
    Compare AES encryption using time-based and butterfly-based dynamic S-Boxes.
    """
    logging.info("Starting encryption comparison...")
    
    # Time-based dynamic S-Box
    sbox_time = time_aes.generate_dynamic_sbox_time()
    start_time = time.time()  # Start time for encryption
    ciphertext_time = time_aes.aes_encrypt_dynamic(plaintext, key, sbox_time)
    end_time = time.time()  # End time for encryption
    logging.info(f"Time-based encryption took {end_time - start_time:.5f} seconds.")
    
    # Butterfly effect-based dynamic S-Box
    sbox_butterfly = butterfly_aes.generate_dynamic_sbox_butterfly()
    start_time = time.time()  # Start time for encryption
    ciphertext_butterfly = butterfly_aes.aes_encrypt_dynamic(plaintext, key, sbox_butterfly)
    end_time = time.time()  # End time for encryption
    logging.info(f"Butterfly-based encryption took {end_time - start_time:.5f} seconds.")
    
    # Print results
    logging.info("\n[Encryption Comparison]")
    print(f"Plaintext: {plaintext.decode('utf-8')}")
    print(f"Time-based Ciphertext: {ciphertext_time.hex()}")
    print(f"Butterfly-based Ciphertext: {ciphertext_butterfly.hex()}")


def compare_entropy(ciphertext_hex):
    """
    Compare entropy calculation for given ciphertext using both methods.
    """
    logging.info("Starting entropy comparison...")

    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        logging.error("Invalid hex format.")
        print("Error: Invalid hex format.")
        return

    # Calculate entropy for both methods
    start_time = time.time()  # Start time for entropy calculation
    entropy_time = time_aes.calculate_entropy(ciphertext)
    end_time = time.time()  # End time for entropy calculation
    logging.info(f"Time-based entropy calculation took {end_time - start_time:.5f} seconds.")

    start_time = time.time()  # Start time for entropy calculation
    entropy_butterfly = butterfly_aes.calculate_entropy(ciphertext)
    end_time = time.time()  # End time for entropy calculation
    logging.info(f"Butterfly-based entropy calculation took {end_time - start_time:.5f} seconds.")

    # Print results
    logging.info("\n[Entropy Comparison]")
    print(f"Ciphertext (Hex): {ciphertext_hex}")
    print(f"Time-based Entropy: {entropy_time}")
    print(f"Butterfly-based Entropy: {entropy_butterfly}")


def main():
    """
    Main function to let users choose between encryption and entropy comparison.
    """
    if len(sys.argv) < 2:
        print("Please provide an option (1 for Encryption, 2 for Entropy Calculation).")
        sys.exit(1)

    choice = sys.argv[1]  # Argument from command line
    
    if choice == "1":
        # Compare encryption
        plaintext_input = input("Enter plaintext (up to 16 characters, will be padded if shorter): ")
        plaintext = plaintext_input.encode('utf-8')
        key_input = input("Enter 16-byte key: ")
        if len(key_input) != 16:
            logging.error("Key must be exactly 16 bytes.")
            print("Error: Key must be exactly 16 bytes.")
            return
        key = key_input.encode('utf-8')
        compare_encryption(plaintext, key)

    elif choice == "2":
        # Compare entropy
        ciphertext_hex = input("Enter ciphertext in hex format: ")
        compare_entropy(ciphertext_hex)

    else:
        logging.error("Invalid option. Please choose either 1 or 2.")
        print("Invalid choice. Please choose either 1 or 2.")


if __name__ == "__main__":
    main()
