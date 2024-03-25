import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class SymmetricCryptography:
    """
    A class for symmetric cryptography operations.

    This class provides methods for generating symmetric keys,
    encrypting and decrypting data using symmetric encryption algorithms.

    Attributes:
        None
    """
    @staticmethod
    def generate_key(key_len: int) -> bytes:
        """
        Generate and return symmetric key.
        
        :param key_len: Length of the key.
        """
        return os.urandom(key_len//8)

    @staticmethod
    def encrypt_text(symmetric_key: bytes, text: bytes) -> bytes:
        """
        Encrypts the text using the provided symmetric key.
        
        :param symmetric_key: Symmetric key.
        :param text: Text to encrypt.
        
        :return: Encrypted text.
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(text) + padder.finalize()
        return iv + encryptor.update(padded_text) + encryptor.finalize()

    @staticmethod
    def decrypt_text(symmetric_key: bytes, encrypted_text: bytes) -> bytes:
        """
        Decrypts the text using the provided symmetric key.
        
        :param symmetric_key: Symmetric key.
        :param encrypted_text: Encrypted text.
        
        :return: Decrypted text.
        """
        iv = encrypted_text[:16]
        encrypted_text = encrypted_text[16:]
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted_text) + unpadder.finalize()