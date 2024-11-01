import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import config


encryption_key = config.encryption_key.encode("utf-8")  # Must be 32 bytes for AES-256

def _generate_random_iv():
    possible = '0123456789'
    return ''.join([possible[os.urandom(1)[0] % len(possible)] for _ in range(16)])

def encrypt(data: str):
    random_iv = _generate_random_iv()
    iv = bytes(random_iv, 'utf-8')
    
    cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(data.encode('utf-8')) + encryptor.finalize()

    encrypted_hex = encrypted.hex()
    iv_hex = iv.hex()

    return encrypted_hex[:10] + iv_hex + encrypted_hex[10:]

def decrypt(hash_str: str):
    iv = bytes.fromhex(hash_str[10:42])
    content = hash_str[:10] + hash_str[42:]

    cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(bytes.fromhex(content)) + decryptor.finalize()

    return decrypted.decode('utf-8')
