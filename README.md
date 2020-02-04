# cryptum
[![Build Status](https://travis-ci.org/AUCR/cryptum.svg?branch=master)](https://travis-ci.org/AUCR/cryptum)
[![codecov](https://codecov.io/gh/AUCR/cryptum/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/AUCR)

## Overview

cryptum is a simple python encryption library that can generate rsa public/private keys and encrypt data for easy 
transport between applications and languages.

## Install with Pip

Example Install with Pip

    pip install cryptum

### Easy cli examples:

#### Help example:

    cryptcli.py --help
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


#### Generate New Private/Public Keys:

    cryptcli.py -g

#### Encrypt "test.txt" with public key example:

    cryptcli.py -e -f test.txt -k pub.txt
    
#### Decrypt test.txt.enc with the private key:    
    
    cryptcli.py -d -f test.txt.enc -k priv.txt


