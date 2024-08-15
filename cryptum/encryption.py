"""Cryptum framework encryption library."""

from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Tuple, Union

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def generate_key() -> Tuple[bytes, bytes]:
    """
    Generate an RSA key pair.

    Returns:
        Tuple[bytes, bytes]: A tuple containing the base64-encoded private and public keys.
    """
    key = RSA.generate(4096)
    private_key = urlsafe_b64encode(key.export_key())
    public_key = urlsafe_b64encode(key.publickey().export_key())
    return private_key, public_key


def decrypt_blob(encrypted_data: Union[bytes, str], private_key: Union[bytes, str]) -> bytes:
    """
    Decrypt RSA + AES encrypted byte data blob from base64encoded string.

    Args:
        encrypted_data (Union[bytes, str]): Encrypted RSA + AES bytes or base64 encoded string.
        private_key (Union[bytes, str]): Base64 encoded RSA private key string or bytes value.

    Returns:
        bytes: Decrypted data.

    Raises:
        ValueError: If the decryption fails or the data is invalid.
    """
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode()
    if isinstance(private_key, str):
        private_key = private_key.encode()

    try:
        rsa_key = RSA.import_key(urlsafe_b64decode(private_key))
        cipher_rsa = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA512)

        enc_session_key = encrypted_data[:512]
        nonce = encrypted_data[512:524]
        cipher_text = encrypted_data[524:-16]
        tag = encrypted_data[-16:]

        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
        data = cipher_aes.decrypt_and_verify(cipher_text, tag)

        return data
    except (ValueError, KeyError):
        raise ValueError("Decryption failed. The data or key may be invalid.")


def encrypt_blob(raw_data: Union[bytes, str], public_key: Union[bytes, str]) -> bytes:
    """
    Encrypt data using RSA + AES.

    Args:
        raw_data (Union[bytes, str]): Data to encrypt.
        public_key (Union[bytes, str]): Base64 encoded RSA public key string or bytes value.

    Returns:
        bytes: Encrypted data.

    Raises:
        ValueError: If the encryption fails or the input is invalid.
    """
    if isinstance(raw_data, str):
        raw_data = raw_data.encode()
    if isinstance(public_key, str):
        public_key = public_key.encode()

    try:
        session_key = get_random_bytes(32)
        pub_key = RSA.import_key(urlsafe_b64decode(public_key))
        cipher_rsa = PKCS1_OAEP.new(pub_key, hashAlgo=SHA512)
        enc_session_key = cipher_rsa.encrypt(session_key)

        nonce = get_random_bytes(12)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
        cipher_text, tag = cipher_aes.encrypt_and_digest(raw_data)

        return enc_session_key + nonce + cipher_text + tag
    except (ValueError, KeyError):
        raise ValueError("Encryption failed. The data or key may be invalid.")
