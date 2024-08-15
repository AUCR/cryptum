# Cryptum

[![Build Status](https://travis-ci.org/AUCR/cryptum.svg?branch=master)](https://travis-ci.org/AUCR/cryptum)
[![codecov](https://codecov.io/gh/AUCR/cryptum/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/AUCR)
[![Test and Publish Cryptum](https://github.com/AUCR/cryptum/actions/workflows/test-and-publish.yml/badge.svg)](https://github.com/AUCR/cryptum/actions/workflows/test-and-publish.yml)

## Overview

Cryptum is a simple Python encryption library that generates RSA public/private keys and encrypts data for easy transport between applications and languages. It provides a straightforward CLI interface for key management and file encryption/decryption.

## Features

- Generate RSA public/private key pairs
- Encrypt files using public keys
- Decrypt files using private keys
- Command-line interface for easy use

## Installation

Install Cryptum using pip:

```bash
pip install cryptum
```

## Usage

### Command-line Interface

Cryptum provides a command-line interface `cryptcli.py` for easy use.

#### Help

```bash
cryptcli.py --help
```

Output:

```
Usage: cryptcli.py [OPTIONS]

Options:
  -e, --encrypt              Encrypt input file.
  -f, --input_file FILENAME  The Input File.
  -k, --input_key FILENAME   The Public/Private Key to use.
  -d, --decrypt              Decrypt input file.
  -o, --output TEXT          Output file.
  -g, --generate             Generate Encryption Keys.
  --version
  --help                     Show this message and exit.
```

#### Generate New Private/Public Keys

```bash
cryptcli.py -g
```

#### Encrypt a File

```bash
cryptcli.py -e -f test.txt -k pub.txt
```

This command encrypts `test.txt` using the public key in `pub.txt`.

#### Decrypt a File

```bash
cryptcli.py -d -f test.txt.enc -k priv.txt
```

This command decrypts `test.txt.enc` using the private key in `priv.txt`.

### Python API

You can also use Cryptum as a Python library in your projects. Here's a basic example:

```python
from cryptum import generate_keys, encrypt_file, decrypt_file

# Generate keys
public_key, private_key = generate_keys()

# Encrypt a file
encrypt_file('input.txt', 'input.txt.enc', public_key)

# Decrypt a file
decrypt_file('input.txt.enc', 'output.txt', private_key)
```

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Continuous Integration and Deployment

This project uses GitHub Actions for continuous integration and deployment. The workflow does the following:

1. Runs tests on multiple Python versions (3.7, 3.8, 3.9, 3.10)
2. Lints the code using flake8
3. Builds the package
4. Publishes the package to PyPI on pushes to the main branch

You can view the detailed workflow in the `.github/workflows/test-and-publish.yml` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### [0.0.3] - 2024-08-15
- Added Python API documentation
- Added proper test suite with pytest
- Improved error handling in CLI

### [0.0.1] - 2020-02-02
- Initial release

## Contact

For questions and support, please open an issue on the GitHub repository.