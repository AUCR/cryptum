"""cryptum config tester."""
# coding=utf-8
import unittest
import json

from base64 import urlsafe_b64decode, urlsafe_b64encode
from cryptum.cryptapp import cryptum_cli
from cryptum.encryption import encrypt_blob, generate_key, decrypt_blob
from click.testing import CliRunner


class CryptumTests(unittest.TestCase):
    """Unittests automated cryptum test case framework."""
    def test_encryption(self):
        test_private_key, test_public_key = generate_key()
        data_test = {"test": "test"}
        data_json_bytes = json.dumps(data_test).encode('utf-8')
        test_encrypted_data = urlsafe_b64encode(encrypt_blob(data_json_bytes, test_public_key))
        test_decrypt_blob = decrypt_blob(urlsafe_b64decode(test_encrypted_data.decode('utf-8')), test_private_key)
        self.assertEqual(test_decrypt_blob, data_json_bytes)

    def test_encryption_cli(self):
        runner = CliRunner()
        result = runner.invoke(cryptum_cli, "--generate").output
        private_key = result[12:4336]
        public_key = result[4347:]
        with open("testprivkey.pem", 'w') as private_key_file:
            private_key_file.write(private_key)
        with open("testpubkey.pem", 'w') as public_key_file:
            public_key_file.write(public_key)
        encrypt_result = runner.invoke(cryptum_cli,
                                       ["--encrypt",
                                        "--input_file=testpubkey.pem",
                                        "--input_key=testpubkey.pem"]
                                       ).output
        with open("test.txt.enc", 'w') as test_encrypted_file:
            test_encrypted_file.write(public_key)
        print(encrypt_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
