from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

class AsymmetricCryptography:
    """
    A class for asymmetric cryptography operations.

    This class provides methods for generating key pairs,
    encrypting and decrypting data using asymmetric encryption algorithms.

    Attributes:
        None
    """
    @staticmethod
    def generate_key_pair(key_size: int) -> tuple:
        """
        Generate an RSA key pair.

        :param key_size: The size of the RSA key in bits.

        :return: A tuple containing the private and public keys.
        """
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def serialize_private_key(private_key: rsa.RSAPrivateKey, path: str) -> None:
        """
        Serialize the private key and save it to a file.

        :param private_key: The private key.
        :param path: The path to save the serialized private key.
        """
        with open(path, 'wb') as key_file:
            key_file.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                     encryption_algorithm=serialization.NoEncryption()))

    @staticmethod
    def serialize_public_key(public_key: rsa.RSAPublicKey, path: str) -> None:
        """
        Serialize the public key and save it to a file.

        :param public_key: The public key.
        :param path: The path to save the serialized public key.
        """
        with open(path, 'wb') as key_file:
            key_file.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PublicFormat.SubjectPublicKeyInfo))

    @staticmethod
    def deserialize_private_key(path: str) -> rsa.RSAPrivateKey:
        """
        Deserialize the private key and return it.

        :param path: The path that contains the serialized private key.
        
        :return: The deserialized private key.
        """
        with open(path, 'rb') as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None)

    @staticmethod
    def deserialize_public_key(path: str) -> rsa.RSAPublicKey:
        """
        Deserialize the public key and return it.

        :param path: The path that contains the serialized public key.
        
        :return: The deserialized public key.
        """
        with open(path, 'rb') as key_file:
            return serialization.load_pem_public_key(key_file.read())

    @staticmethod
    def encrypt_with_public_key(public_key: rsa.RSAPublicKey, text: bytes) -> bytes:
        """
        Encrypts ntext using the provided public key.

        :param public_key: The RSA public key used for encryption.
        :param text: The text to be encrypted.

        :return: The ciphertext produced by the encryption process.
        """
        return public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))

    @staticmethod
    def decrypt_with_private_key(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
        """
        Decrypts ciphertext using the provided private key.

        :param private_key: The RSA private key used for decryption.
        :param ciphertext: The ciphertext to be decrypted.

        :return: The text produced by the decryption process.
        """
        return private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                            algorithm=hashes.SHA256(), label=None))