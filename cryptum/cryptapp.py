"""The cryptum python cli python package."""
# coding=utf-8
import click
import logging
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptum.encryption import encrypt_blob, decrypt_blob, generate_key
from yaml_info.yamlinfo import YamlInfo

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@click.group()
@click.option('--debug/--no-debug')
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(YamlInfo("projectinfo.yml", "projectinfo", "LICENSE"))
    ctx.exit()


@click.command()
@click.option("--encrypt", "-e", is_flag=True, help="Encrypt input file.")
@click.option("--input_file", "-f", type=click.File('rb'), help="The Input File.")
@click.option("--input_key", "-k", type=click.File('rb'), help="The Public/Private Key to use.")
@click.option("--decrypt", "-d", is_flag=True, help="Decrypt input file.")
@click.option("--output", "-o", help="Output file.")
@click.option("--generate", "-g", is_flag=True, help="Generate Encryption Keys.")
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cryptum_cli(encrypt, input_file, input_key, decrypt, output, generate):
    if encrypt:
        input_data = input_file.read()
        key_data = input_key.read()
        encrypted_data = urlsafe_b64encode(encrypt_blob(input_data, key_data))
        print(encrypted_data.decode('utf-8'))
    if decrypt:
        input_data = input_file.read()
        key_data = input_key.read()
        decrypted_data = decrypt_blob(urlsafe_b64decode(input_data.decode('utf-8')), key_data)
        print(decrypted_data.decode('utf-8'))
    if generate:
        private_key, public_key = generate_key()
        print("Private Key:" + private_key.decode('utf-8') + "\n" + "Public Key:" + public_key.decode('utf-8'))
