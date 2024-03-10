import argparse
import logging
import os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1


logging.basicConfig(level=logging.INFO)


def key_generation(symmetric_key_path: str, key_len: int, public_path: str, private_path: str) -> None:
    try:
        symmetric_key = os.urandom(key_len)
        
        asymmetric_keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4196
        )
        private_key = asymmetric_keys
        public_key = asymmetric_keys.public_key()
        try:
            with open(public_path, 'wb') as public_out:
                    public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo))

            with open(private_path, 'wb') as private_out:
                    private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()))
            logging.info(f"Keys successfully generated and write to files: {public_path}, {private_path}.")
        except Exception as ex:
            logging.error(f"Can't serialize asymmetric keys: {ex}.")
        
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            OAEP(
                mgf=MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        try:
            with open(f"{symmetric_key_path[:-4]}_{key_len}.txt", 'wb') as key_file:
                key_file.write(encrypted_symmetric_key)
            logging.info(f"Key successfully generated and write to file: {symmetric_key_path[:-4]}_{key_len}.txt")
        except Exception as ex:
            logging.error(f"Can't serialize symmetric key: {ex}.")
        
    except Exception as ex:
        logging.error(f"An error occurred while generating the key: {ex}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An application for generate symmetric and asymmetric keys.")
    
    parser.add_argument(
        "--len",
        type=int,
        default=256,
        help="Encryption key length."
    )
    parser.add_argument(
        "--symmetric_path",
        type=str,
        default=os.path.join('lab_3','symmetric_keys','symmetric.txt'),
        help="Encryption symmetric key path."
    )
    parser.add_argument(
        "--asymmetric_public",
        type=str,
        default=os.path.join('lab_3','asymmetric_keys','public.pem'),
        help="Encryption asymmetric public key path."
    )
    parser.add_argument(
        "--asymmetric_private",
        type=str,
        default=os.path.join('lab_3','asymmetric_keys','private.pem'),
        help="Encryption asymmetric private key path."
    )
    
    args = parser.parse_args()

    key_generation(args.symmetric_path, args.len, args.asymmetric_public, args.asymmetric_private)