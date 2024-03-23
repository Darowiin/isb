import os
import logging

from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logging.basicConfig(level=logging.INFO)

class HybridEncryption:
    def __init__(self, text_path, private_key_path, public_key_path, symmetric_key_path, encrypted_text_path, decrypted_text_path, key_len):
        self.text_path = text_path
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path
        self.symmetric_key_path = symmetric_key_path
        self.encrypted_text_path = encrypted_text_path
        self.decrypted_text_path = decrypted_text_path
        self.key_len = key_len


    def generate_keys(self):
        try:
            symmetric_key = os.urandom(int(self.key_len/8))
            
            asymmetric_keys = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            try:
                self._serialization_asymmetric_keys(asymmetric_keys)
                logging.info(f"Keys successfully generated and write to files: {self.public_key_path}, {self.private_key_path}.")
            except Exception as ex:
                logging.error(f"Can't serialize asymmetric keys: {ex}.")
            
            encrypted_symmetric_key = asymmetric_keys.public_key().encrypt(
                symmetric_key,
                OAEP(
                    mgf=MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            try:
                self._serialization_symmetric_key(encrypted_symmetric_key)
                logging.info(f"Key successfully generated and write to file: {self.symmetric_key_path[:-4]}_{self.key_len}.txt")
            except Exception as ex:
                logging.error(f"Can't serialize symmetric key: {ex}.")
            
        except Exception as ex:
            logging.error(f"An error occurred while generating the key: {ex}")


    def encrypt_text(self):
        try:
            d_symmetric_key = self._deserialization_symmetric_key()
        
            text = bytes(self._read_text(self.text_path,"r","UTF-8"),"UTF-8")
            
            c_text = self._encrypt_text_with_symmetric_key(d_symmetric_key,text)
            
            self._write_text(c_text,self.encrypted_text_path)
            
            logging.info("The text was successfully encrypted and written to a file.")
        except Exception as ex:
            logging.error(f"An error occurred while encrypting and writing text to a file: {ex}.",exc_info=True)


    def decrypt_text(self):
        try:
            d_symmetric_key = self._deserialization_symmetric_key()
            
            c_text = self._read_text(self.encrypted_text_path,"rb")
                
            unpadded_dc_text = self._decrypt_text_with_symmetric_key(d_symmetric_key,c_text)
            
            self._write_text(unpadded_dc_text,self.decrypted_text_path)
            logging.info("The text was successfully decrypted and written to a file.")
        except Exception as ex:
            logging.error(f"An error occurred while decrypting and writing text to a file: {ex}.",exc_info=True)


    def _encrypt_text_with_symmetric_key(self, symmetric_key, text):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(text) + padder.finalize()
        return iv + encryptor.update(padded_text) + encryptor.finalize()


    def _decrypt_text_with_symmetric_key(self, symmetric_key, encrypted_text):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_dc_text = unpadder.update(decrypted_text)+unpadder.finalize()
        return unpadded_dc_text
    
    
    def _serialization_asymmetric_keys(self, asymmetric_keys):
        with open(self.public_key_path, 'wb') as public_out:
            public_out.write(asymmetric_keys.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo))

        with open(self.private_key_path, 'wb') as private_out:
            private_out.write(asymmetric_keys.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()))
    
    
    def _deserialization_asymmetric_keys(self) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        with open(self.public_key_path, 'rb') as pem_in:
            public_bytes = pem_in.read()
            d_public_key = serialization.load_pem_public_key(public_bytes)
        with open(self.private_key_path, 'rb') as pem_in:
            private_bytes = pem_in.read()
            d_private_key = serialization.load_pem_private_key(private_bytes,password=None,)
        return d_private_key, d_public_key
    
    
    def _serialization_symmetric_key(self, encrypted_symmetric_key) -> None:
        with open(f"{self.symmetric_key_path[:-4]}_{self.key_len}.txt", 'wb') as key_file:
                    key_file.write(encrypted_symmetric_key)
    
    
    def _deserialization_symmetric_key(self) -> bytes:
        with open(f"{self.symmetric_key_path[:-4]}_{self.key_len}.txt", mode='rb') as key_file: 
            encrypted_symmetric_key = key_file.read()
        d_private_key, _ = self._deserialization_asymmetric_keys()
        return d_private_key.decrypt(encrypted_symmetric_key,OAEP(mgf=MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    
    
    def _read_text(self, text_path, mode, encoding=None):
        with open(text_path, mode=mode,encoding=encoding) as text_file:
                return text_file.read()
    
    
    def _write_text(self, text, text_path) -> None:
        with open(text_path, "wb") as text_file:
                text_file.write(text)