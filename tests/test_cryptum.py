"""Cryptum config tester."""

import json
import unittest
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Tuple
from os import remove
from click.testing import CliRunner

from cryptum.cryptapp import cryptum_cli
from cryptum.encryption import encrypt_blob, generate_key, decrypt_blob


class CryptumTests(unittest.TestCase):
    """Unittests automated cryptum test case framework."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.runner = CliRunner()

    def test_encryption(self) -> None:
        """Test the encryption and decryption process."""
        test_private_key, test_public_key = generate_key()
        data_test = {"test": "test"}
        data_json_bytes = json.dumps(data_test).encode('utf-8')

        test_encrypted_data = urlsafe_b64encode(encrypt_blob(data_json_bytes, test_public_key))
        test_decrypt_blob = decrypt_blob(urlsafe_b64decode(test_encrypted_data), test_private_key)

        self.assertEqual(test_decrypt_blob, data_json_bytes)

    def test_encryption_cli(self) -> None:
        """Test the CLI interface for encryption and key generation."""
        private_key, public_key = self._generate_keys_via_cli()
        self._write_keys_to_files(private_key, public_key)

        encrypt_result = self.runner.invoke(
            cryptum_cli,
            ["--encrypt", "--input_file=testpubkey.pem", "--input_key=testpubkey.pem"]
        ).output

        with open("test.txt.enc", 'w') as test_encrypted_file:
            test_encrypted_file.write(public_key)

        self.assertIsNotNone(encrypt_result)
        print(encrypt_result)
        # Remove the test data
        [remove(f) for f in ["testprivkey.pem", "testpubkey.pem", "test.txt.enc"]]

    def _generate_keys_via_cli(self) -> Tuple[str, str]:
        """Generate keys using the CLI and return them."""
        result = self.runner.invoke(cryptum_cli, "--generate").output
        private_key = result[12:4336]
        public_key = result[4347:]
        return private_key, public_key

    def _write_keys_to_files(self, private_key: str, public_key: str) -> None:
        """Write the generated keys to files."""
        with open("testprivkey.pem", 'w') as private_key_file:
            private_key_file.write(private_key)
        with open("testpubkey.pem", 'w') as public_key_file:
            public_key_file.write(public_key)


if __name__ == '__main__':
    unittest.main(verbosity=2)
