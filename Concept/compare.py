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
    Run the encryption 10 times and calculate average time.
    """
    logging.info("Starting encryption comparison...")

    time_based_times = []
    butterfly_based_times = []

    for _ in range(10):
        # Time-based dynamic S-Box
        sbox_time = time_aes.generate_dynamic_sbox_time()
        start_time = time.time()  # Start time for encryption
        ciphertext_time = time_aes.aes_encrypt_dynamic(plaintext, key, sbox_time)
        end_time = time.time()  # End time for encryption
        time_based_times.append(end_time - start_time)

        # Butterfly effect-based dynamic S-Box
        sbox_butterfly = butterfly_aes.generate_dynamic_sbox_butterfly()
        start_time = time.time()  # Start time for encryption
        ciphertext_butterfly = butterfly_aes.aes_encrypt_dynamic(plaintext, key, sbox_butterfly)
        end_time = time.time()  # End time for encryption
        butterfly_based_times.append(end_time - start_time)

    avg_time_based = sum(time_based_times) / 10
    avg_butterfly_based = sum(butterfly_based_times) / 10

    # Print results
    logging.info("\n[Encryption Comparison]")
    print(f"Plaintext: {plaintext.decode('utf-8')}")
    print(f"Average Time-based Ciphertext: {ciphertext_time.hex()}")
    print(f"Average Butterfly-based Ciphertext: {ciphertext_butterfly.hex()}")
    print(f"Average Time-based Encryption Time: {avg_time_based:.5f} seconds")
    print(f"Average Butterfly-based Encryption Time: {avg_butterfly_based:.5f} seconds")

def compare_entropy(ciphertext_hex):
    """
    Compare entropy calculation for given ciphertext using both methods.
    Run the entropy calculation 10 times and calculate average time.
    """
    logging.info("Starting entropy comparison...")

    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        logging.error("Invalid hex format.")
        print("Error: Invalid hex format.")
        return

    time_based_times = []
    butterfly_based_times = []

    for _ in range(10):
        # Calculate entropy for time-based method
        start_time = time.time()  # Start time for entropy calculation
        entropy_time = time_aes.calculate_entropy(ciphertext)
        end_time = time.time()  # End time for entropy calculation
        time_based_times.append(end_time - start_time)

        # Calculate entropy for butterfly-based method
        start_time = time.time()  # Start time for entropy calculation
        entropy_butterfly = butterfly_aes.calculate_entropy(ciphertext)
        end_time = time.time()  # End time for entropy calculation
        butterfly_based_times.append(end_time - start_time)

    avg_entropy_time = sum(time_based_times) / 10
    avg_entropy_butterfly = sum(butterfly_based_times) / 10

    # Print results
    logging.info("\n[Entropy Comparison]")
    print(f"Ciphertext (Hex): {ciphertext_hex}")
    print(f"Average Time-based Entropy: {entropy_time}")
    print(f"Average Butterfly-based Entropy: {entropy_butterfly}")
    print(f"Average Time-based Entropy Calculation Time: {avg_entropy_time:.5f} seconds")
    print(f"Average Butterfly-based Entropy Calculation Time: {avg_entropy_butterfly:.5f} seconds")

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
