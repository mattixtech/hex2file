"""
hex2file.py
Matthew Brooks, 2018

Utility for writing hex to a file.
"""
import binascii


def _sanitize(hex_str):
    """
    Sanitize string input before attempting to write to file.

    :param hex_str: the string input to sanitize
    :return: the sanitized string
    """

    return "".join(hex_str.replace("0x", "").split())


def write_str(hex_str, file_path, append=False):
    """
    Write a hex string to a file as hex.

    :param hex_str: the string containing the hex
    :param file_path: the path to the file to write
    :param append:  whether to append or overwrite
    :return: None
    """

    if hex_str is not None:
        mode = "wb"
        if append:
            mode += "+"
        with open(file_path, mode) as f:
            for line in iter(hex_str.splitlines()):
                if line:
                    f.write(binascii.unhexlify(_sanitize(line)))


def write_from_file(text_file_path, file_path, append=False):
    """
    Writes the hex (in ascii format) contained in the given file to the given
    output file path.

    :param text_file_path: the path to the input file
    :param file_path: the path to the file to write
    :param append: whether to append or overwrite
    :return: None
    """

    with open(text_file_path, 'r') as input_file:
        write_str(input_file.read(), file_path, append)
