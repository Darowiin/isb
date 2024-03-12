import argparse
import os

from generation_keys import key_generation
from data_encryption import text_encryption
from data_decryption import text_decryption

def main():
    parser = argparse.ArgumentParser(description="Single entry point for key generation, encryption, and decryption.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation',
                       action='store_true',
                       help='Run key generation mode.')
    group.add_argument('-enc', '--encryption',
                       action='store_true',
                       help='Run encryption mode.')
    group.add_argument('-dec', '--decryption',
                       action='store_true',
                       help='Run decryption mode.')

    args = parser.parse_args()

    if args.generation:
        key_generation(
            os.path.join('lab_3', 'symmetric_keys', 'symmetric.txt'),
            256,
            os.path.join('lab_3', 'asymmetric_keys', 'public.pem'),
            os.path.join('lab_3', 'asymmetric_keys', 'private.pem')
        )

    elif args.encryption:
        text_encryption(
            os.path.join('lab_3', 'text.txt'),
            os.path.join('lab_3', 'asymmetric_keys', 'private.pem'),
            os.path.join('lab_3', 'symmetric_keys', 'symmetric_256.txt'),
            os.path.join('lab_3', 'encrypted_text.txt')
        )

    elif args.decryption:
        text_decryption(
            os.path.join('lab_3', 'encrypted_text.txt'),
            os.path.join('lab_3', 'asymmetric_keys', 'private.pem'),
            os.path.join('lab_3', 'symmetric_keys', 'symmetric_256.txt'),
            os.path.join('lab_3', 'decrypted_text.txt')
        )

if __name__ == "__main__":
    main()