"""Cryptum framework encryption library."""
# coding=utf-8

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from base64 import urlsafe_b64decode, urlsafe_b64encode


def generate_key() -> [bytes, bytes]:
    """Return python bytes value of rsa private key and public key."""
    key = RSA.generate(4096)
    private_key = urlsafe_b64encode(key.export_key())
    public_key = urlsafe_b64encode(key.publickey().export_key())
    return private_key, public_key


def decrypt_blob(encrypted_data, private_key) -> bytes:
    """Decrypt RSA + AES encrypted byte data blob from base64encoded string.
    :ivar encrypted_data: encrypted rsa + aes bytes.
    :encrypted_data encrypted_data: bytes
    :ivar private_key: urlsafe base64encoded rsa private key string value.
    :private_key private_key: string
    """
    rsa_key = RSA.importKey(urlsafe_b64decode(private_key))
    # Set hashAlgo=SHA512 to override default sha1 library use.
    rsa_key = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA512)
    json_byte_value = b''
    decrypted_key = rsa_key.decrypt(encrypted_data[:512])
    cipher_text = encrypted_data[524:-16]
    nonce = encrypted_data[512:524]
    tag = encrypted_data[-16:]
    # Decrypt the AES data with the decrypted session key.
    cipher_aes = AES.new(decrypted_key, AES.MODE_GCM, nonce)
    data = cipher_aes.decrypt_and_verify(cipher_text, tag)
    json_byte_value += data
    return json_byte_value


def encrypt_blob(raw_data, public_key) -> bytes:
    """Return RSA + AES encrypted byte data from raw data input.
    :ivar raw_data: Bytes rsa + aes data.
    :raw_data raw_data: bytes
    :ivar public_key: urlsafe base64encoded rsa public key string value.
    :public_key public_key: string"""
    decrypted_bytes = b''
    session_key = get_random_bytes(32)
    # Encrypt the session key with the public RSA key
    pub_key = RSA.import_key(urlsafe_b64decode(public_key))
    cipher_rsa = PKCS1_OAEP.new(pub_key, hashAlgo=SHA512)
    enc_session_key = cipher_rsa.encrypt(session_key)
    # Encrypt the data with the AES session key using 12 random bytes because that's the default of golang.
    nonce = get_random_bytes(12)
    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
    cipher_text, tag = cipher_aes.encrypt_and_digest(raw_data)
    decrypted_bytes += enc_session_key
    decrypted_bytes += nonce
    decrypted_bytes += cipher_text
    decrypted_bytes += tag
    return decrypted_bytes
