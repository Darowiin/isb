import argparse
import logging
import os

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.serialization import load_pem_private_key


logging.basicConfig(level=logging.INFO,filemode="w",filename="lab_3/py_log_2.log")


def text_decryption(encrypted_text_path: str, private_key_path: str, symmetric_key_path: str, decrypted_text_path: str) -> None:
    """
    Decrypt text using asymmetric and symmetric keys and save the result to a file.

    :param encrypted_text_path: Path to the encrypted file containing the text to be decrypted.
    :param private_key_path: Path to the asymmetric private encryption key.
    :param symmetric_key_path: Path to the symmetric encrypted key.
    :param decrypted_text_path: Path to the new decrypted text.
    """
    logging.info("Starting the text decryption.")
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
        with open(encrypted_text_path, "rb") as text_file:
            c_text = text_file.read()
            
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(d_symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(c_text) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text)+unpadder.finalize()
        with open(decrypted_text_path, "wb") as decryption_file:
            decryption_file.write(unpadded_dc_text)
        logging.info("The text was successfully decrypted and written to a file.")
    except Exception as ex:
        logging.error(f"An error occurred while decrypting and writing text to a file: {ex}.",exc_info=True)
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Applications for decrypting text using the symmetric AES method.")
    
    parser.add_argument(
        "--encrypted_text",
        type=str,
        default=os.path.join("lab_3","encrypted_text.txt"),
        help="The path to the encrypted file containing the text to be decrypted."
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
        "--decryption_text",
        type=str,
        default=os.path.join("lab_3","decrypted_text.txt"),
        help="The path to the new encrypted text."
    )
    
    args = parser.parse_args()
    
    text_decryption(args.encrypted_text,args.private_key,args.symmetric_key,args.decryption_text)