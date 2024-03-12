import argparse
import logging
import os

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.serialization import load_pem_private_key


logging.basicConfig(level=logging.INFO,filemode="w",filename="lab_3/py_log.log")


def text_encryption(text_path: str, private_key_path: str, symmetric_key_path: str, encryption_text_path: str) -> None:
    """
    Encrypt text using asymmetric and symmetric keys and save the result to a file.

    :param text_path: Path to the input file containing the text to be encrypted.
    :param private_key_path: Path to the asymmetric private encryption key.
    :param symmetric_key_path: Path to the symmetric encrypted key.
    :param encryption_text_path: Path to the new encrypted text.
    """
    logging.info("Starting the text encryption.")
    try:
        with open(private_key_path, 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes,password=None,)
        logging.info("The private key has been successfully serialized.")
    except Exception as ex:
        logging.error(f"An error occurred while deserialization of the private key",exc_info=True)
    
    try:
        with open(symmetric_key_path, 'rb') as symmetric_file:
                symmetric_key = symmetric_file.read()
        d_symmetric_key = d_private_key.decrypt(symmetric_key,OAEP(mgf=MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        logging.info("Symmetric key successfully decrypted.")
    except Exception as ex:
        logging.error(f"An error occurred while decryption of the symmetric key: {ex}.",exc_info=True)
    
    try:
        with open(text_path, "r", encoding="UTF-8") as text_file:
            text = bytes(text_file.read(), encoding="UTF-8")
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(text)+padder.finalize()
        logging.info("The text was successfully padded.")
    except Exception as ex:
        logging.error(f"An error occurred while padding the text: {ex}.",exc_info=True)
    
    try:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(d_symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        with open(encryption_text_path, "wb") as encryption_file:
            encryption_file.write(c_text)
        logging.info("The text was successfully encrypted and written to a file.")
    except Exception as ex:
        logging.error(f"An error occurred while encrypting and writing text to a file: {ex}.",exc_info=True)
     
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Applications for encrypting text using the symmetric AES method.")
    
    parser.add_argument(
        "--original_text",
        type=str,
        default=os.path.join("lab_3","text.txt"),
        help="The path to the input file containing the text to be encrypted."
    )
    parser.add_argument(
        "--private_key",
        type=str,
        default=os.path.join("lab_3","asymmetric_keys","private.pem"),
        help="The path to the asymmetric private encryption key."
    )
    parser.add_argument(
        "--symmetric_key",
        type=str,
        default=os.path.join("lab_3","symmetric_keys","symmetric_256.txt"),
        help="The path to the symmetric encrypted key."
    )
    parser.add_argument(
        "--encryption_text",
        type=str,
        default=os.path.join("lab_3","encrypted_text.txt"),
        help="The path to the new encrypted text."
    )
    
    args = parser.parse_args()
    
    text_encryption(args.original_text,args.private_key,args.symmetric_key,args.encryption_text)