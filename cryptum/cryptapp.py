"""The cryptum python cli package."""

import logging
from base64 import urlsafe_b64encode, urlsafe_b64decode
from typing import Optional, TextIO

import click

from cryptum.encryption import encrypt_blob, decrypt_blob, generate_key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@click.group()
@click.option('--debug/--no-debug', help="Enable or disable debug mode.")
def cli(debug: bool) -> None:
    """Main CLI group for cryptum."""
    click.echo(f'Debug mode is {"on" if debug else "off"}')

def print_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """Print the version of cryptum."""
    if not value or ctx.resilient_parsing:
        return
    # Note: YamlInfo has been removed as it's no longer needed
    click.echo("cryptum version 0.0.1")  # Replace with actual version
    ctx.exit()

@click.command()
@click.option("--encrypt", "-e", is_flag=True, help="Encrypt input file.")
@click.option("--input_file", "-f", type=click.File('rb'), help="The Input File.")
@click.option("--input_key", "-k", type=click.File('rb'), help="The Public/Private Key to use.")
@click.option("--decrypt", "-d", is_flag=True, help="Decrypt input file.")
@click.option("--output", "-o", help="Output file.")
@click.option("--generate", "-g", is_flag=True, help="Generate Encryption Keys.")
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cryptum_cli(
    encrypt: bool,
    input_file: Optional[TextIO],
    input_key: Optional[TextIO],
    decrypt: bool,
    output: Optional[str],
    generate: bool
) -> None:
    """
    Cryptum CLI for encryption, decryption, and key generation.

    This function handles the main CLI operations for the cryptum package.
    It can encrypt or decrypt files, and generate encryption keys.

    Args:
        encrypt (bool): Flag to encrypt the input file.
        input_file (TextIO): The input file to be processed.
        input_key (TextIO): The public/private key file to be used.
        decrypt (bool): Flag to decrypt the input file.
        output (str): The output file path.
        generate (bool): Flag to generate new encryption keys.
    """
    if encrypt and input_file and input_key:
        input_data = input_file.read()
        key_data = input_key.read()
        encrypted_data = urlsafe_b64encode(encrypt_blob(input_data, key_data))
        click.echo(encrypted_data.decode('utf-8'))

    if decrypt and input_file and input_key:
        input_data = input_file.read()
        key_data = input_key.read()
        decrypted_data = decrypt_blob(urlsafe_b64decode(input_data.decode('utf-8')), key_data)
        click.echo(decrypted_data.decode('utf-8'))

    if generate:
        private_key, public_key = generate_key()
        click.echo(f"Private Key: {private_key.decode('utf-8')}\nPublic Key: {public_key.decode('utf-8')}")

    if output:
        # TODO: Implement output file writing
        click.echo(f"Output will be written to {output}")

if __name__ == '__main__':
    cryptum_cli()
